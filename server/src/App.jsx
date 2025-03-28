import { Routes, Route } from "react-router-dom";
import Sidebar from "./Sidebar";
import Home from "./pages/Home";
import Rules from "./pages/Rules";
import AddRule from "./pages/AddRule";

function App() {
  return (
    <div className="flex">
      <Sidebar />
      <div className="ml-64 p-6 flex-1">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/:ip/rules" element={<Rules />} />
          <Route path="/:ip/add-rule" element={<AddRule />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
