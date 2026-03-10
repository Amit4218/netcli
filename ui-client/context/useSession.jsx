import React, { createContext, useContext, useState } from "react";

export const SessionContext = createContext();

export const SessionContextProvider = ({ children }) => {
  const [session, setSession] = useState(null);

  return (
    <SessionContext.Provider value={{ session, setSession }}>
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
