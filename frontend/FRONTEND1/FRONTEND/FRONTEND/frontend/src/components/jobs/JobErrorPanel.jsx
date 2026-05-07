import Card from "../common/Card";
import ErrorMessage from "../common/ErrorMessage";

export default function JobErrorPanel({ message, status }) {
  return (
    <Card className="border-rose-300 bg-rose-100/70">
      <h2 className="mb-3 text-lg font-black text-rose-700">Optimization Loop Interrupted</h2>
      <ErrorMessage message={message || `Job ended with status: ${status}`} />
    </Card>
  );
}
