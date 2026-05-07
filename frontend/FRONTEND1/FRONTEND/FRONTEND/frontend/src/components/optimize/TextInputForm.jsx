import Textarea from "../common/Textarea";

export default function TextInputForm({ value, onChange, error }) {
  return <Textarea label="Marketing Text" value={value} onChange={(event) => onChange(event.target.value)} error={error} placeholder="Paste or draft the text NISF should optimize..." />;
}
