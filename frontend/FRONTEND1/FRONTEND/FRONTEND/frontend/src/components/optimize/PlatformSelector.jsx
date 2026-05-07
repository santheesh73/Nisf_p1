import Select from "../common/Select";
import { PLATFORMS } from "../../utils/constants";

export default function PlatformSelector({ value, onChange }) {
  return <Select label="Platform" options={PLATFORMS} value={value} onChange={(e) => onChange(e.target.value)} />;
}
