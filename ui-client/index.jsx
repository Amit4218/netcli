#!/usr/bin/env node

import React from "react";
import { render } from "ink";
import App from "./App.jsx";
import { SessionContextProvider } from "./context/useSession.jsx";

// Enter alternate screen
process.stdout.write("\x1b[?1049h");
process.stdout.write("\x1b[?25l"); // hide cursor

const { waitUntilExit } = render(
  <SessionContextProvider>
    <App />
  </SessionContextProvider>,
);

// This runs when useApp().exit() is called
waitUntilExit().then(() => {
  process.stdout.write("\x1b[?25h"); // show cursor
  process.stdout.write("\x1b[?1049l"); // leave alternate screen
});
