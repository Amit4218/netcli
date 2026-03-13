import React, { createContext, useContext, useState } from "react";

export const SessionContext = createContext();

export const SessionContextProvider = ({ children }) => {
  const [session, setSession] = useState(null);
  const [isLoading, setIsLoading] = useState(false)
  const [movies, setMovies] = useState([])
  const [episodes, setEpisodes] = useState([])
  const [currentWatching, setCurrentWatching] = useState([])


  return (
    <SessionContext.Provider value={{ 
      session, setSession, 
      isLoading, setIsLoading,
      movies, setMovies, 
      episodes, setEpisodes,
      currentWatching,
      setCurrentWatching 
    }}>
      {children}
    </SessionContext.Provider>
  );
};

export const useSession = () => {
  const ctx = useContext(SessionContext);
  if (!ctx)
    throw new Error("useSession must be used inside SessionContextProvider");
  return ctx;
};
