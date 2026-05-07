import Input from "../common/Input";
import Select from "../common/Select";

export default function OptimizationSettings({ values, onChange }) {
  const update = (key, value) => onChange({ ...values, [key]: Number(value) });
  return (
    <div className="grid gap-4 md:grid-cols-3">
      <Select label="Max Iterations" options={[1, 2, 3, 4, 5].map((v) => ({ value: v, label: `${v}` }))} value={values.max_iterations} onChange={(e) => update("max_iterations", e.target.value)} />
      <Input label="Target Score" type="number" min="1" max="100" value={values.target_score} onChange={(e) => update("target_score", e.target.value)} />
      <Select label="Variant Count" options={[3, 4, 5].map((v) => ({ value: v, label: `${v}` }))} value={values.variant_count} onChange={(e) => update("variant_count", e.target.value)} />
    </div>
  );
}
