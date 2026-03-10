import { TitledBox } from "@mishieck/ink-titled-box";
import { Text } from "ink";
import React, { useEffect, useState } from "react";

function Header() {
  const [now, setNow] = useState(new Date().toLocaleTimeString());

  // Clock
  useEffect(() => {
    const interval = setInterval(() => {
      setNow(new Date().toLocaleTimeString());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <TitledBox
      borderStyle="round"
      paddingX={3}
      flexDirection="row"
      borderColor={"green"}
      borderDimColor={true}
      justifyContent="space-between"
      titles={["Net-cli"]}
      titleJustify="center"
    >
      <Text>📽</Text>
      <Text>Search & Watch anything via terminal</Text>
      <Text>{now}</Text>
    </TitledBox>
  );
}

export default Header;
