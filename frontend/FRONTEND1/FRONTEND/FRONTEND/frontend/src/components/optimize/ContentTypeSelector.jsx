import Select from "../common/Select";
import { CONTENT_TYPES } from "../../utils/constants";

export default function ContentTypeSelector({ value, onChange }) {
  return <Select label="Content Type" options={CONTENT_TYPES} value={value} onChange={(e) => onChange(e.target.value)} />;
}
