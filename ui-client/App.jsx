import { Box, Text, useInput, useApp, useFocusManager } from "ink";
import useTerminalSize from "./hooks/useTerminalSize";
import Header from "./components/Header";
import Input from "./components/Input";
import Shortcuts from "./components/Shortcuts";
import Movies from "./components/Movies";
import React, { useEffect } from "react";

function App() {
  const { exit } = useApp();
  const { width, height } = useTerminalSize();
  const { focus } = useFocusManager();

  useEffect(() => {
    focus("input");
  }, []);

  // Terminal size guard
  if (width < 50 || height < 10) {
    return (
      <Box>
        <Text color="red">Terminal too small. Please resize.</Text>
      </Box>
    );
  }

  // Keyboard navigation
  useInput((input) => {
    if (input === "q") {
      exit();
    }
  });
  return (
    <Box
      width="100%"
      height={42}
      flexDirection="column"
      padding={1}
      borderColor="blue"
      borderDimColor={true}
      borderStyle="round"
    >
      {/* Header */}
      <Header />

      {/* Search Input */}
      <Input />

      {/* Results */}
      <Movies />

      {/* Shortcuts */}
      <Shortcuts />
    </Box>
  );
}

export default App;
