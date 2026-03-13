import React, { useState } from "react";
import { useSession } from "../context/useSession";
import { Box, Text, useInput, useApp, useFocus } from "ink";
import { TitledBox } from "@mishieck/ink-titled-box";
import axios from "axios";
import { ScrollList } from "ink-scroll-list";
import Loader from "./Loader";

function SelectLanguage() {
  const { currentWatching, isLoading, setIsLoading } = useSession();
  const { exit } = useApp();
  const { isFocused } = useFocus({ id: "languages" });

  const [selectedIndex, setSelectedIndex] = useState(0);
  const [success, setSuccess] = useState(false);
  const [selectedMovie, setSelectedMovie] = useState(null);

  const handleSelect = async () => {
    try {
      const res = await axios.post(`http://localhost:6789/play`, {
        link: selectedMovie.url,
        referrer: selectedMovie.header.referrer,
      });
      if (res.data.success) {
        setSuccess(true);
      }
    } catch (err) {
      setIsLoading(false);
    } finally {
      setIsLoading(false);
    }
  };

  useInput((input, key) => {
    if (!isFocused) return;
    if (currentWatching.length === 0) return;
    if (isLoading) return;

    if (key.downArrow) {
      setSelectedIndex((prev) =>
        prev === currentWatching.length - 1 ? 0 : prev + 1,
      );
    }

    if (key.upArrow) {
      setSelectedIndex((prev) =>
        prev === 0 ? currentWatching.length - 1 : prev - 1,
      );
    }

    if (key.return) {
      const selected = currentWatching[selectedIndex];
      if (!selected) return;

      setSelectedMovie(selected);
      setIsLoading(true);
      handleSelect(selected);
    }

    if (key.escape) exit();
  });

  return (
    <>
      {isLoading && selectedMovie && (
        <Loader titleText={`Searching for ${selectedMovie}`} />
      )}

      {
        <TitledBox
          flexGrow={1}
          width="100%"
          height={20}
          flexDirection="column"
          borderStyle="round"
          borderColor={isFocused ? "cyan" : "gray"}
          titles={["Please select a language"]}
          titleJustify="center"
        >
          {!success && (
            <ScrollList
              selectedIndex={selectedIndex}
              flexDirection="column"
              paddingX={1}
            >
              {currentWatching.map((m, idx) => (
                <Box key={idx} height={1}>
                  <Text color={idx === selectedIndex ? "green" : "white"}>
                    {idx === selectedIndex ? "> " : "  "}
                    {m.language}
                  </Text>
                </Box>
              ))}
            </ScrollList>
          )}
          {success && (
            <Box flexGrow={1} alignItems="center" justifyContent="center">
              <Text dimColor>Playing now...</Text>
            </Box>
          )}
        </TitledBox>
      }
    </>
  );
}

export default SelectLanguage;
