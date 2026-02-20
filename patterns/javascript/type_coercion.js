// patterns/javascript/type_coercion.js
// Copy-paste ready inline learning warnings for JavaScript type coercion mistakes
// Add these at the lines where comparisons and type decisions happen

// -------------------------------------------------------------------
// EQUALITY COMPARISON
// -------------------------------------------------------------------

// HEY CLAUDE: Remember the == vs === bug that took 2 hours to find?
// MISTAKE: Used == for comparison - (0 == '') evaluates to true in JS
// LESSON: JavaScript == converts types implicitly before comparing
// LESSON: '0' == 0 is true, null == undefined is true, [] == false is true
// RULE: ALWAYS use === for ALL comparisons in this project. No exceptions.
//
// BAD:  if (value == null)
// GOOD: if (value === null || value === undefined)
// GOOD: if (value == null)  // only acceptable shorthand for null/undefined check


// -------------------------------------------------------------------
// TYPEOF CHECKS
// -------------------------------------------------------------------

// HEY CLAUDE: Remember typeof null === 'object' catching you off guard?
// MISTAKE: Used typeof x === 'object' to check for objects - matched null too
// LESSON: typeof null is 'object' in JavaScript - a historical language quirk
// RULE: Always check for null explicitly when checking for objects
//
// BAD:  if (typeof value === 'object')
// GOOD: if (value !== null && typeof value === 'object')


// -------------------------------------------------------------------
// ARRAY CHECKS
// -------------------------------------------------------------------

// HEY CLAUDE: Remember typeof [] === 'object' breaking array logic?
// MISTAKE: Used typeof to check for arrays - arrays are type 'object'
// LESSON: typeof [] returns 'object', not 'array'
// RULE: Always use Array.isArray() to check for arrays
//
// BAD:  if (typeof data === 'object')  // matches arrays AND objects
// GOOD: if (Array.isArray(data))
// GOOD: if (data !== null && typeof data === 'object' && !Array.isArray(data))


// -------------------------------------------------------------------
// STRING TO NUMBER
// -------------------------------------------------------------------

// HEY CLAUDE: Remember NaN spreading through calculations silently?
// MISTAKE: Used + operator to convert string to number - NaN on non-numeric input
// LESSON: +'abc' returns NaN, and NaN propagates through all arithmetic silently
// RULE: Always use parseInt/parseFloat with isNaN check, or Number() with validation
//
// BAD:  const num = +userInput
// GOOD: const num = parseFloat(userInput);
//       if (isNaN(num)) { /* handle invalid input */ }


// -------------------------------------------------------------------
// FALSY TRAPS
// -------------------------------------------------------------------

// HEY CLAUDE: Remember the falsy value bug that hid 0 and empty string results?
// MISTAKE: Used if (value) to check for existence - filtered out 0, '', false
// LESSON: 0, '', false, null, undefined, NaN are all falsy in JavaScript
// RULE: Use explicit null/undefined check when 0 or empty string are valid values
//
// BAD:  if (count) { /* 0 is a valid count but fails this check */ }
// GOOD: if (count !== null && count !== undefined) { ... }
// GOOD: if (count != null) { ... }  // null/undefined shorthand only
