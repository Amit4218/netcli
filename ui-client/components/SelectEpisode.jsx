import React, { useEffect, useState } from "react";
import { useSession } from "../context/useSession";
import { Box, Text, useInput, useApp, useFocus } from "ink";
import { TitledBox } from "@mishieck/ink-titled-box";
import axios from "axios";
import { ScrollList } from "ink-scroll-list";
import Loader from "./Loader";

function SelectEpisode() {
  const { session } = useSession();
  const { exit } = useApp();
  const { isFocused } = useFocus({ id: "episodes" });

  const [episode, setEpisodes] = useState(session["episodes"]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [success, setSuccess] = useState(false);1

  const [isLoading, setIsLoading] = useState(false);
  const [selectedEpisode, setSelectedEpisode] = useState(null);

  const handleSelect = async () => {
    try {
      const res = await axios.post(`http://localhost:6789/get`, {
        link: session.base_link,
        ep_id: selectedEpisode,
      });
      if (res.data.success) {
        setSuccess(true);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useInput((input, key) => {
    if (!isFocused) return;
    if (episode.length === 0) return;
    if (isLoading) return;

    if (key.downArrow) {
      setSelectedIndex((prev) => (prev === episode.length - 1 ? 0 : prev + 1));
    }

    if (key.upArrow) {
      setSelectedIndex((prev) => (prev === 0 ? episode.length - 1 : prev - 1));
    }

    if (key.return) {
      const selected = episode[selectedIndex];
      if (!selected) return;

      setSelectedEpisode(selected);
      setIsLoading(true);
      handleSelect(selected);
    }

    if (key.escape) exit();
  });

  return (
    <>
      {isLoading && selectedEpisode && (
        <Loader titleText={`Searching for ${selectedEpisode}`} />
      )}

      {
        <TitledBox
          flexGrow={1}
          width="100%"
          height={20}
          flexDirection="column"
          borderStyle="round"
          borderColor={isFocused ? "cyan" : "gray"}
          titles={[session.message]}
          titleJustify="center"
        >
          {!success && (
            <ScrollList
              selectedIndex={selectedIndex}
              flexDirection="column"
              paddingX={1}
            >
              {episode.map((ep, idx) => (
                <Box key={`${ep.title}-${idx}`} height={1}>
                  <Text color={idx === selectedIndex ? "green" : "white"}>
                    {idx === selectedIndex ? "> " : "  "}
                    {ep}
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

export default SelectEpisode;
