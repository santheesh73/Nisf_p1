import Select from "../common/Select";
import { TONES } from "../../utils/constants";

export default function ToneSelector({ value, onChange }) {
  return <Select label="Tone" options={TONES} value={value} onChange={(e) => onChange(e.target.value)} />;
}
