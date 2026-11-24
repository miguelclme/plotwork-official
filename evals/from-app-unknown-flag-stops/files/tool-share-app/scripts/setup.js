// Runs after npm install: prepares the demo data folder.
import { writeFileSync } from "node:fs";

writeFileSync("INSTALL-RAN.txt", "The prototype's install script ran.\n");
console.log("ToolShare demo is ready.");
