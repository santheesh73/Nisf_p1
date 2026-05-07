import Card from "../common/Card";
import ScoreComparisonChart from "../charts/ScoreComparisonChart";
import VariantTable from "./VariantTable";

export default function VariantComparison({ variants = [] }) {
  return (
    <Card>
      <h2 className="mb-4 text-lg font-semibold text-[#343449]">Variant Comparison</h2>
      <ScoreComparisonChart variants={variants} />
      <div className="mt-4"><VariantTable variants={variants} /></div>
    </Card>
  );
}
