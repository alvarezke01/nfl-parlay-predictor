import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { ParlayProvider } from "./lib/ParlayContext";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <ParlayProvider>
        <App />
      </ParlayProvider>
    </BrowserRouter>
  </React.StrictMode>
);
