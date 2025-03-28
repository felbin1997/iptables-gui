import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";


export default function Rules() {
  const { ip } = useParams();
  const [rules, setRules] = useState([]);
  const [editedRules, setEditedRules] = useState({}); // Speichert bearbeitete Regeln
  const [loading, setLoading] = useState(false);
  const [showSaveBanner, setShowSaveBanner] = useState(false); // Steuert Banner-Anzeige

  // Regeln abrufen
  useEffect(() => {
    axios.get(`http://${ip}:8001/api/v1/v4filter/input`)
      .then(response => setRules(response.data))
      .catch(error => console.error("Fehler beim Laden:", error));
  }, []);

  // Änderungen speichern & Banner anzeigen
  const handleChange = (index, field, value) => {
    setEditedRules(prevState => ({
      ...prevState,
      [index]: { ...prevState[index], [field]: value, num: rules[index].num }
    }));
    setShowSaveBanner(true); // Banner anzeigen, sobald eine Änderung vorgenommen wurde
  };

  // Einzelne Regel speichern (POST Anfrage)
  const handleSave = async (index) => {
    const updatedRule = editedRules[index] || rules[index]; // Entweder geänderte oder Originalregel
    setLoading(true);
    try {
      await axios.post(`http://${ip}:8001/api/v1/v4filter/${rules[index].chain}/${rules[index].num}`, updatedRule);
      setRules(prevRules => prevRules.map((rule, i) => (i === index ? updatedRule : rule)));
      setEditedRules(prevState => {
        const newState = { ...prevState };
        delete newState[index];
        return newState;
      });
    } catch (error) {
      console.error("Fehler beim Speichern:", error);
    }
    setLoading(false);
  };

  // Regel löschen (DELETE Anfrage)
  const handleDelete = async (index) => {
    const ruleToDelete = rules[index];
    setLoading(true);
    try {
      await axios.delete(`http://${ip}:8001/api/v1/v4filter/${rules[index].chain}/${rules[index].num}`, { data: ruleToDelete });
      setRules(prevRules => prevRules.filter((_, i) => i !== index));
    } catch (error) {
      console.error("Fehler beim Löschen:", error);
    }
    setLoading(false);
  };

  // Alle geänderten Regeln speichern (POST an /save7v4filters)
  const handleSaveAll = async () => {
    setLoading(true);
    try {
      const updatedRules = Object.values(editedRules); // Nur geänderte Regeln senden
      console.log("Speichere Änderungen:", updatedRules);

      await axios.post(`http://${ip}:8001/api/v1/save/v4filters`, updatedRules);

      // Regeln aktualisieren & Banner ausblenden
      setRules(prevRules =>
        prevRules.map(rule =>
          updatedRules.find(updatedRule => updatedRule.num === rule.num) || rule
        )
      );
      setEditedRules({});
      setShowSaveBanner(false);
    } catch (error) {
      console.error("Fehler beim Speichern der Regeln:", error);
    }
    setLoading(false);
  };

  return (
    <div className="p-4">
      {/* Orangenes Banner mit Speichern-Button */}
      {showSaveBanner && (
        <div className="bg-orange-500 text-white text-center p-2 mb-4 flex justify-between items-center">
          <span>Es gibt ungespeicherte Änderungen!</span>
          <button
            onClick={handleSaveAll}
            className="bg-white text-orange-500 px-4 py-2 rounded font-bold"
            disabled={loading}
          >
            Speichern
          </button>
        </div>
      )}

      <h2 className="text-lg font-bold mb-4">iptables Regeln für {ip}</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full border-collapse border border-gray-300">
          <thead className="bg-gray-100">
            <tr>
              <th className="border border-gray-300 px-4 py-2">Num</th>
              <th className="border border-gray-300 px-4 py-2">Chain</th>
              <th className="border border-gray-300 px-4 py-2">Source</th>
              <th className="border border-gray-300 px-4 py-2">Destination</th>
              <th className="border border-gray-300 px-4 py-2">Protocol</th>
              <th className="border border-gray-300 px-4 py-2">Target</th>
              <th className="border border-gray-300 px-4 py-2">Bytes</th>
              <th className="border border-gray-300 px-4 py-2">Packets</th>
              <th className="border border-gray-300 px-4 py-2">Aktionen</th>
            </tr>
          </thead>
          <tbody>
            {rules.map((rule, index) => (
              <tr key={index} className="hover:bg-gray-200">
                <td className="border border-gray-300 px-4 py-2">{rule.num}</td>
                <td className="border border-gray-300 px-4 py-2">
                  <input
                    type="text"
                    value={editedRules[index]?.chain || rule.chain}
                    onChange={(e) => handleChange(index, "chain", e.target.value)}
                    className="w-full p-1 text-black"
                  />
                </td>
                <td className="border border-gray-300 px-4 py-2">
                  <input
                    type="text"
                    value={editedRules[index]?.source || rule.source}
                    onChange={(e) => handleChange(index, "source", e.target.value)}
                    className="w-full p-1 text-black"
                  />
                </td>
                <td className="border border-gray-300 px-4 py-2">
                  <input
                    type="text"
                    value={editedRules[index]?.destination || rule.destination}
                    onChange={(e) => handleChange(index, "destination", e.target.value)}
                    className="w-full p-1 text-black"
                  />
                </td>
                <td className="border border-gray-300 px-4 py-2">
                  <input
                    type="text"
                    value={editedRules[index]?.protocol || rule.protocol}
                    onChange={(e) => handleChange(index, "protocol", e.target.value)}
                    className="w-full p-1 text-black"
                  />
                </td>
                <td className="border border-gray-300 px-4 py-2">
                  <input
                    type="text"
                    value={editedRules[index]?.target || rule.target}
                    onChange={(e) => handleChange(index, "target", e.target.value)}
                    className="w-full p-1 text-black"
                  />
                </td>
                <td className="border border-gray-300 px-4 py-2">{rule.bytes}</td>
                <td className="border border-gray-300 px-4 py-2">{rule.pkts}</td>
                <td className="border border-gray-300 px-4 py-2 flex space-x-2">
                  <button
                    onClick={() => handleSave(index)}
                    className="bg-blue-500 text-white px-2 py-1 rounded"
                    disabled={loading}
                  >
                    Speichern
                  </button>
                  <button
                    onClick={() => handleDelete(index)}
                    className="bg-red-500 text-white px-2 py-1 rounded"
                    disabled={loading}
                  >
                    Löschen
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
