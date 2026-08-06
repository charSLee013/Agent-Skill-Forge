#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

const event = process.argv[2];
const projectRoot = path.resolve(
  process.env.PONYTAIL_PROJECT_ROOT ||
  process.env.CLAUDE_PROJECT_DIR ||
  process.cwd(),
);
const statePath = path.join(projectRoot, '.codex', 'ponytail', '.ponytail-active');
const skillPath = path.join(__dirname, '..', 'skills', 'productivity', 'ponytail', 'SKILL.md');

const isCopilot = Boolean(process.env.COPILOT_PLUGIN_DATA);
const isCodex = !isCopilot && (
  process.env.PONYTAIL_HOST === 'codex' || Boolean(process.env.PLUGIN_DATA)
);
const isQoder = !isCopilot && !isCodex && Boolean(process.env.QODER_SESSION_ID);

// This is a persistent enable latch, not a per-session mode. Nothing clears it
// except one of the explicit cancellation commands handled below.
function isActive() {
  return fs.existsSync(statePath);
}

function activate() {
  fs.mkdirSync(path.dirname(statePath), { recursive: true });
  fs.writeFileSync(statePath, 'active\n', 'utf8');
}

function deactivate() {
  try {
    fs.unlinkSync(statePath);
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }
}

function instructions() {
  try {
    const body = fs.readFileSync(skillPath, 'utf8').replace(/^---[\s\S]*?---\s*/, '');
    return `PONYTAIL ACTIVE\n\n${body}`;
  } catch (_) {
    return [
      'PONYTAIL ACTIVE',
      '',
      'Implement the approved behavior with the least code that preserves correctness.',
      'Read and trace the real flow first. Reuse existing mechanisms, standard',
      'libraries, native platform features, and installed dependencies before',
      'writing new code. Never shrink scope or weaken required evidence.',
    ].join('\n');
  }
}

function writeOutput(hookEvent, active, context = '') {
  if (isCopilot) {
    const output = hookEvent === 'SessionStart' && context
      ? { additionalContext: context }
      : {};
    process.stdout.write(JSON.stringify(output));
    return;
  }

  if (isCodex) {
    const output = { systemMessage: active ? 'PONYTAIL:ACTIVE' : 'PONYTAIL:OFF' };
    if (context) {
      output.hookSpecificOutput = {
        hookEventName: hookEvent,
        additionalContext: context,
      };
    }
    process.stdout.write(JSON.stringify(output));
    return;
  }

  if (isQoder) {
    const output = {};
    if (context) {
      output.hookSpecificOutput = {
        hookEventName: hookEvent,
        additionalContext: context,
      };
    }
    process.stdout.write(JSON.stringify(output));
    return;
  }

  if (hookEvent === 'SubagentStart') {
    process.stdout.write(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: hookEvent,
        additionalContext: context,
      },
    }));
    return;
  }

  process.stdout.write(context);
}

function emitRules(hookEvent) {
  writeOutput(hookEvent, true, instructions());
}

function isDeactivateCommand(prompt) {
  const command = prompt.trim().toLowerCase().replace(/[.!?\s]+$/, '');
  return command === 'stop ponytail' ||
    command === 'normal mode' ||
    /^[/@$]ponytail(?::ponytail)?\s+off$/.test(command);
}

function isActivateCommand(prompt) {
  return /^[/@$]ponytail(?::ponytail)?(?:\s|$)/i.test(prompt.trim());
}

function handlePrompt() {
  let input = '';
  let finished = false;

  function finish() {
    if (finished) return;
    finished = true;

    try {
      const payload = JSON.parse(input.replace(/^\uFEFF/, ''));
      const prompt = String(payload.prompt || '');

      if (isDeactivateCommand(prompt)) {
        deactivate();
        writeOutput('UserPromptSubmit', false, 'PONYTAIL OFF');
      } else if (isActivateCommand(prompt)) {
        activate();
        emitRules('UserPromptSubmit');
      } else if (isQoder && isActive()) {
        emitRules('UserPromptSubmit');
      }
    } catch (_) {
      // Hooks are best-effort and must never block a session on malformed input.
    }
  }

  process.stdin.on('data', (chunk) => { input += chunk; });
  process.stdin.on('end', finish);
  process.stdin.on('error', () => { finish(); process.exit(0); });
  setTimeout(() => { finish(); process.exit(0); }, 1000).unref();
}

try {
  if (event === 'session') {
    if (isActive()) emitRules('SessionStart');
  } else if (event === 'subagent') {
    if (isActive()) emitRules(isQoder ? 'PreToolUse' : 'SubagentStart');
  } else if (event === 'prompt') {
    handlePrompt();
  } else {
    process.exitCode = 2;
  }
} catch (_) {
  // Hook failures must not interrupt the host session.
}
