// Tells a tool's owner that someone wants to borrow it.
// For the demo this only writes to the console: no email is sent.
export function notifyOwner(tool, borrower, loan) {
  console.log(
    `[demo] Email to owner of "${tool.name}": ${borrower.name} would like it from ${loan.from} to ${loan.to}.`
  );
  return Promise.resolve({ sent: true });
}
