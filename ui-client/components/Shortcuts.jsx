import { TitledBox } from "@mishieck/ink-titled-box";
import { Text } from "ink";
import React from "react";

function Shortcuts() {
  return (
    <TitledBox
      borderStyle="round"
      paddingX={1}
      alignItems="center"
      borderColor={"green"}
      borderDimColor={true}
      justifyContent="center"
      marginTop={1}
      titles={["Shortcuts"]}
      titleJustify="center"
    >
      <Text>↑ ↓ → navigate | Enter → select | q → quit</Text>
    </TitledBox>
  );
}

export default Shortcuts;
