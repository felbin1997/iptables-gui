import { useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import API_BASE_PATH from "../config";

export default function AddRule() {
  const { ip } = useParams();
  const [formData, setFormData] = useState({
    chain: "INPUT",
    source: "",
    destination: "",
    protocol: "tcp",
    target: "ACCEPT",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.put(`http://${ip}:8001/${API_BASE_PATH}/v4filter/${formData.chain}`, formData);
      setMessage("Regel erfolgreich hinzugefügt!");
    } catch (error) {
      console.error("Fehler beim Hinzufügen der Regel:", error);
      setMessage("Fehler beim Speichern der Regel.");
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h2 className="text-2xl font-bold mb-4">Regel für {ip} hinzufügen</h2>

      {message && <p className="mb-4 text-green-500">{message}</p>}

      <form onSubmit={handleSubmit} className="bg-gray-800 p-4 rounded-lg text-white">
        <div className="mb-3">
          <label className="block">Chain</label>
          <select name="chain" value={formData.chain} onChange={handleChange} className="w-full p-2 text-black">
            <option value="INPUT">INPUT</option>
            <option value="OUTPUT">OUTPUT</option>
            <option value="FORWARD">FORWARD</option>
          </select>
        </div>

        <div className="mb-3">
          <label className="block">Quelle (Source)</label>
          <input type="text" name="source" value={formData.source} onChange={handleChange} 
            className="w-full p-2 text-black" placeholder="z.B. 192.168.1.100" required />
        </div>

        <div className="mb-3">
          <label className="block">Ziel (Destination)</label>
          <input type="text" name="destination" value={formData.destination} onChange={handleChange} 
            className="w-full p-2 text-black" placeholder="z.B. 192.168.1.200" required />
        </div>

        <div className="mb-3">
          <label className="block">Protokoll</label>
          <select name="protocol" value={formData.protocol} onChange={handleChange} className="w-full p-2 text-black">
            <option value="tcp">TCP</option>
            <option value="udp">UDP</option>
            <option value="icmp">ICMP</option>
          </select>
        </div>

        <div className="mb-3">
          <label className="block">Zielaktion (Target)</label>
          <select name="target" value={formData.target} onChange={handleChange} className="w-full p-2 text-black">
            <option value="ACCEPT">ACCEPT</option>
            <option value="DROP">DROP</option>
            <option value="REJECT">REJECT</option>
          </select>
        </div>

        <button type="submit" className="bg-blue-500 px-4 py-2 rounded-lg mt-4">
          Regel hinzufügen
        </button>
      </form>
    </div>
  );
}
