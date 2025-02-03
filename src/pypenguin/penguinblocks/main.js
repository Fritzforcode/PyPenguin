import { parse } from "./syntax.js";
import * as fs from "fs";

// Get command-line arguments
const args = process.argv.slice(2); // Ignore "node" and script name
// Use arguments to determine input code or file
if (args.length < 2) {
  console.error("Usage: node main.js <codeString> <outputPath>");
  process.exit(1);
}

const code = args[0]; // First argument is the code string
const outputPath = args[1]; // Second argument is the output file path

// Parse the code and write to the output file
const doc = parse(code, {});
fs.writeFileSync(outputPath, JSON.stringify(doc));
