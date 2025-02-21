import Canvas from "./Canvas";

function App() {
  return (
    <>
      <div className="flex h-screen w-screen flex-row">
        <div className="flex h-full w-96 flex-none flex-col items-center gap-2 p-4">
          <h1 className="text-3xl font-semibold">Truss Calculator</h1>
          <hr className="w-full" />
          <h2 className="text-xl font-medium">Node</h2>
          <hr className="w-full" />
        </div>
        <div className="flex-auto">
          <Canvas />
        </div>
      </div>
    </>
  );
}

export default App;
