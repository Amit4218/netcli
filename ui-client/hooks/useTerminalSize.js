import { useStdout } from "ink";
import { useEffect, useState } from "react";

function useTerminalSize() {
  const { stdout } = useStdout();
  const [size, setSize] = useState({
    width: stdout.columns,
    height: stdout.rows,
  });

  useEffect(() => {
    const handler = () =>
      setSize({ width: stdout.columns, height: stdout.rows });

    stdout.on("resize", handler);
    return () => stdout.off("resize", handler);
  }, [stdout]);

  return size;
}

export default useTerminalSize;
