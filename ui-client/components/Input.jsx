import { useFocus, useFocusManager, useInput } from "ink";
import TextInput from "ink-text-input";
import React, { useState } from "react";
import { useSession } from "../context/useSession";
import Loader from "./Loader";
import { TitledBox } from "@mishieck/ink-titled-box";
import axios from "axios";

function Input() {
  const [movieName, setMovieName] = useState("");
  const { isFocused } = useFocus({ id: "input", isFocusable: true });
  const { focus } = useFocusManager();
  const { setMovies, setIsLoading, isLoading } = useSession();

  const handleInput = async (val) => {
    if (!movieName.trim()) return;
    setMovieName(val);
    setIsLoading(true);

    const res = await axios.get(`http://localhost:6789/${movieName}`);
    setMovies(res.data);
    focus("movies");
    setMovieName("");
    setIsLoading(false);
  };

  useInput((input) => {
    if (input && isFocused) {
      return;
    }
  });

  return (
    <>
      {!isLoading && (
        <TitledBox
          paddingX={1}
          borderStyle="round"
          width="40%"
          marginX="30%"
          borderColor={isFocused ? "blue" : ""}
          titles={["Search"]}
          titleJustify="center"
        >
          <TextInput
            focus={isFocused}
            value={movieName}
            onChange={setMovieName}
            placeholder="Enter your movie name: "
            onSubmit={(val) => {
              handleInput(val);
            }}
          />
        </TitledBox>
      )}
      {isLoading && isFocused && (
        <Loader titleText={`Searching for '${movieName}' `} />
      )}
    </>
  );
}

export default Input;
