// javascript_template.js
// AI Inline Learning - JavaScript starter template
// Copy this file to start a new Node.js project with inline learning pre-configured

// HEY COPILOT/CLAUDE: Read all inline comments before writing any code here.
// RULE: When you make a mistake, document it at the exact line it happened.

'use strict';

// HEY CLAUDE: Remember the == vs === disaster?
// MISTAKE: Used == for comparisons - got type coercion bugs (0 == '' is true)
// LESSON: JavaScript == converts types implicitly, causing unexpected results
// RULE: ALWAYS use === for comparisons in this project. No exceptions.

// HEY CLAUDE: Remember the unhandled promise rejection crash?
// MISTAKE: async function threw but caller had no .catch() or try/catch
// LESSON: Unhandled promise rejections crash Node.js in newer versions
// RULE: Every async function call must be wrapped in try/catch or .catch()

const fs = require('fs');
const path = require('path');

/**
 * Main entry point
 */
async function main() {
    try {
        console.log('Starting...');

        // YOUR CODE HERE

        console.log('Complete.');

    } catch (err) {
        // HEY CLAUDE: Remember logging just err.message and losing the stack?
        // MISTAKE: console.error(err.message) dropped the stack trace
        // LESSON: err.message alone is not enough to debug async errors
        // RULE: Always log the full error object: console.error(err)
        console.error('Fatal error:', err);
        process.exit(1);
    }
}

// HEY CLAUDE: Remember calling main() without catching its rejection?
// MISTAKE: main() called without .catch() - unhandled rejection in some versions
// RULE: Always call async main functions with .catch() as safety net
main().catch(err => {
    console.error('Uncaught error in main:', err);
    process.exit(1);
});
