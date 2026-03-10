import { TitledBox } from "@mishieck/ink-titled-box";
import Spinner from "ink-spinner";
import React from "react";

function Loader({ titleText }) {
  return (
    <TitledBox
      paddingX={1}
      flexDirection="column"
      borderStyle="round"
      borderColor={"yellow"}
      width="40%"
      marginX="30%"
      alignItems="center"
      justifyContent="center"
      titles={[titleText]}
      titleJustify="center"
      padding={1}
    >
      <Spinner type="bouncingBall" />
    </TitledBox>
  );
}

export default Loader;
