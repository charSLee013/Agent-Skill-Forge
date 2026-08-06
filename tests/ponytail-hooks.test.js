const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const root = path.join(__dirname, '..');
const hook = path.join(root, 'hooks', 'ponytail.js');

function run(event, projectRoot, prompt = '', extraEnv = {}) {
  return spawnSync(process.execPath, [hook, event], {
    env: {
      ...process.env,
      PONYTAIL_HOST: 'codex',
      PONYTAIL_PROJECT_ROOT: projectRoot,
      ...extraEnv,
    },
    input: prompt ? JSON.stringify({ prompt }) : '',
    encoding: 'utf8',
  });
}

function tempProject(t) {
  const projectRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ponytail-'));
  t.after(() => fs.rmSync(projectRoot, { recursive: true, force: true }));
  return projectRoot;
}

function statePath(projectRoot) {
  return path.join(projectRoot, '.codex', 'ponytail', '.ponytail-active');
}

test('project config registers the three persistence events', () => {
  const config = JSON.parse(fs.readFileSync(path.join(root, '.codex', 'hooks.json'), 'utf8'));
  const expected = {
    SessionStart: 'session',
    SubagentStart: 'subagent',
    UserPromptSubmit: 'prompt',
  };

  for (const [event, argument] of Object.entries(expected)) {
    const handlers = config.hooks[event].flatMap((group) => group.hooks);
    assert.equal(handlers.length, 1);
    assert.match(handlers[0].command, new RegExp(`hooks/ponytail\\.js\\" ${argument}$`));
  }
});

test('Ponytail remains off until explicitly invoked', (t) => {
  const projectRoot = tempProject(t);

  assert.equal(run('session', projectRoot).stdout, '');
  assert.equal(run('prompt', projectRoot, 'Review the Ponytail documentation.').stdout, '');
  assert.equal(fs.existsSync(statePath(projectRoot)), false);
});

test('manual activation latches Ponytail on and injects one ruleset', (t) => {
  const projectRoot = tempProject(t);
  const result = run('prompt', projectRoot, '$ponytail implement the approved issue');

  assert.equal(result.status, 0);
  assert.equal(fs.readFileSync(statePath(projectRoot), 'utf8'), 'active\n');

  const output = JSON.parse(result.stdout);
  const context = output.hookSpecificOutput.additionalContext;
  assert.equal(output.systemMessage, 'PONYTAIL:ACTIVE');
  assert.match(context, /least code that preserves correctness/i);
  assert.match(context, /Do not replace Wayfinder/);
  assert.doesNotMatch(context, /lite|ultra/i);
});

test('session restore and subagent inheritance reuse the active ruleset', (t) => {
  const projectRoot = tempProject(t);
  run('prompt', projectRoot, '$ponytail');

  for (const event of ['session', 'subagent']) {
    const result = run(event, projectRoot);
    const output = JSON.parse(result.stdout);
    assert.equal(output.systemMessage, 'PONYTAIL:ACTIVE');
    assert.match(output.hookSpecificOutput.additionalContext, /## Correctness/);
  }
});

test('ordinary work and hook failures cannot clear the enable latch', (t) => {
  const projectRoot = tempProject(t);
  run('prompt', projectRoot, '$ponytail');

  run('prompt', projectRoot, 'Implement the next approved issue.');
  run('prompt', projectRoot, 'Add a normal mode toggle to this component.');
  run('session', projectRoot);
  run('subagent', projectRoot);
  spawnSync(process.execPath, [hook, 'prompt'], {
    env: {
      ...process.env,
      PONYTAIL_HOST: 'codex',
      PONYTAIL_PROJECT_ROOT: projectRoot,
    },
    input: 'not json',
    encoding: 'utf8',
  });

  assert.equal(fs.readFileSync(statePath(projectRoot), 'utf8'), 'active\n');
  assert.equal(JSON.parse(run('session', projectRoot).stdout).systemMessage, 'PONYTAIL:ACTIVE');
});

test('host adapters keep their required context shapes', (t) => {
  const projectRoot = tempProject(t);
  run('prompt', projectRoot, '$ponytail');

  const claude = run('session', projectRoot, '', {
    PONYTAIL_HOST: '',
    PLUGIN_DATA: '',
  });
  assert.match(claude.stdout, /^PONYTAIL ACTIVE/);

  const copilot = run('session', projectRoot, '', {
    PONYTAIL_HOST: '',
    PLUGIN_DATA: '',
    COPILOT_PLUGIN_DATA: '1',
  });
  assert.match(JSON.parse(copilot.stdout).additionalContext, /^PONYTAIL ACTIVE/);

  const qoder = run('subagent', projectRoot, '', {
    PONYTAIL_HOST: '',
    PLUGIN_DATA: '',
    QODER_SESSION_ID: '1',
  });
  const qoderOutput = JSON.parse(qoder.stdout).hookSpecificOutput;
  assert.equal(qoderOutput.hookEventName, 'PreToolUse');
  assert.match(qoderOutput.additionalContext, /^PONYTAIL ACTIVE/);
});

test('normal mode clears project state', (t) => {
  const projectRoot = tempProject(t);
  run('prompt', projectRoot, '/ponytail');

  const result = run('prompt', projectRoot, 'normal mode');

  assert.equal(JSON.parse(result.stdout).systemMessage, 'PONYTAIL:OFF');
  assert.equal(fs.existsSync(statePath(projectRoot)), false);
  assert.equal(run('session', projectRoot).stdout, '');
});
