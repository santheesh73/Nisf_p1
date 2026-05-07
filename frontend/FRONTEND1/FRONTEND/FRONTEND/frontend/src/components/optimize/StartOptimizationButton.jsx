import { Play } from "lucide-react";
import Button from "../common/Button";

export default function StartOptimizationButton({ loading }) {
  return <Button type="submit" disabled={loading}><Play className="h-4 w-4" />{loading ? "Starting Loop" : "Start Optimization Loop"}</Button>;
}
