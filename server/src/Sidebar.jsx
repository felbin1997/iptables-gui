import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { ChevronDown, ChevronUp } from "lucide-react"; // Icons für das Dropdown (npm install lucide-react)

export default function Sidebar() {
  const [pcs, setPcs] = useState([]);       // PC-Liste von /neighbours
  const [openPcs, setOpenPcs] = useState({}); // Steuert das Dropdown für Filter

  // PCs laden
  useEffect(() => {
    axios.get("http://10.3.0.70:8001/api/v1/neighbours")
      .then(response => setPcs(response.data.data))
      .catch(error => console.error("Fehler beim Laden der PCs:", error));
  },[]);
  const loadFilters = (pc) => {
    setOpenPcs(prevState => ({ ...prevState, [pc]: !prevState[pc] })); // Öffnet oder schließt das Menü
  };

  return (
    <div className="w-64 h-screen bg-gray-800 text-white fixed top-0 left-0 p-4">
      <h2 className="text-lg font-bold">Menü</h2>
      <nav className="mt-4">
        <Link to="/" className="block py-2 px-4 hover:bg-gray-700">Home</Link>

        {/* Verfügbare PCs */}
        <h3 className="text-sm font-semibold mt-4">Verfügbare PCs</h3>
        {pcs.length > 0 ? (
          pcs.map((pc, index) => (
            <div key={index} className="mt-4">
              <button key={index}
                className="flex justify-between w-full py-2 px-4 hover:bg-gray-700 focus:outline-none mt-4"
                onClick={() => loadFilters(pc)}
              >
              {pc}
                {openPcs[pc] ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
              </button>
              {openPcs[pc] && (
                <div className="ml-4">
                  <Link to={`/${pc}/rules`} className="block py-2 px-4 hover:bg-gray-700">
                    Regeln anzeigen
                  </Link>
                  <Link to={`/${pc}/add-rule`} className="block py-2 px-4 hover:bg-gray-700">
                    Regel hinzufügen
                  </Link>

                </div>
              )}
          </div>

          ))
        ) : (
          <p className="text-gray-400 px-4">Keine PCs verfügbar</p>
        )}
      </nav>
    </div>
  );
}
