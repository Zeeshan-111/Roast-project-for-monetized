import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import RoastGenerator from "./components/RoastGenerator";
import { Toaster } from "./components/ui/toaster";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<RoastGenerator />} />
        </Routes>
      </BrowserRouter>
      <Toaster />
    </div>
  );
}

export default App;