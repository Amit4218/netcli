import React, { useEffect, useState } from "react";
import { useSession } from "../context/useSession";
import { Box, Text, useInput, useApp, useFocus } from "ink";
import { TitledBox } from "@mishieck/ink-titled-box";
import axios from "axios";
import { ScrollList } from "ink-scroll-list";
import Loader from "./Loader";
import SelectEpisode from "./SelectEpisode";

function Movies() {
  const { session, setSession } = useSession();
  const { exit } = useApp();
  const { isFocused } = useFocus({ id: "movies" });

  const [movies, setMovies] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [hideMovies, setHideMovies] = useState(false);

  const [isLoading, setIsLoading] = useState(false);
  const [selectedMovie, setSelectedMovie] = useState(null);

  const handleSelect = async (link) => {
    try {
      const res = await axios.post("http://localhost:6789/verify", {
        url: link,
      });

      if (res.status == 200) {
        setSession(res.data);
        setHideMovies(true);
        focus("episodes");
      }
    } catch (err) {
      console.error(err);
      setMovies([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (Array.isArray(session)) {
      setMovies(session);
      setSelectedIndex(0);
    }
  }, [session]);

  useInput((input, key) => {
    if (!isFocused) return;
    if (movies.length === 0) return;
    if (isLoading) return;

    if (key.downArrow) {
      setSelectedIndex((prev) => (prev === movies.length - 1 ? 0 : prev + 1));
    }

    if (key.upArrow) {
      setSelectedIndex((prev) => (prev === 0 ? movies.length - 1 : prev - 1));
    }

    if (key.return) {
      const selected = movies[selectedIndex];
      if (!selected) return;

      setSelectedMovie(selected);
      setIsLoading(true);
      handleSelect(selected.link);
    }

    if (key.escape) exit();
  });

  return (
    <>
      {isLoading && selectedMovie && (
        <Loader titleText={`Searching for ${selectedMovie.title}`} />
      )}

      {!hideMovies && (
        <TitledBox
          flexGrow={1}
          width="100%"
          height={20}
          flexDirection="column"
          borderStyle="round"
          borderColor={isFocused ? "cyan" : "gray"}
          titles={[" Movie Results "]}
          titleJustify="center"
        >
          {movies.length === 0 ? (
            <Box flexGrow={1} alignItems="center" justifyContent="center">
              <Text dimColor>No movies found</Text>
            </Box>
          ) : (
            <ScrollList
              selectedIndex={selectedIndex}
              flexDirection="column"
              paddingX={1}
            >
              {movies.map((movie, idx) => (
                <Box key={`${movie.title}-${idx}`} height={1}>
                  <Text color={idx === selectedIndex ? "green" : "white"}>
                    {idx === selectedIndex ? "> " : "  "}
                    {movie.title}
                  </Text>
                </Box>
              ))}
            </ScrollList>
          )}
        </TitledBox>
      )}
      {hideMovies && <SelectEpisode />}
    </>
  );
}

export default Movies;
