import React from "react";
import { useState } from "react";
import { Button } from "./components/ui/button";

const App: React.FC = () => {
  const [count, setCount] = useState(0);

  return (
    <div className="dark">
      <Button>hihihihi</Button>
      <h1>Vite + React</h1>
      <div>
        <button onClick={() => setCount(count => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p>Click on the Vite and React logos to learn more</p>
    </div>
  );
};

export default App;
