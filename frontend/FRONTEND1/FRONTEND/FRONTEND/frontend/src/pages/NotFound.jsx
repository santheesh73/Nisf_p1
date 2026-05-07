import { Link } from "react-router-dom";
import Button from "../components/common/Button";
import Card from "../components/common/Card";

export default function NotFound() {
  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <Card className="max-w-lg text-center">
        <p className="text-sm font-bold uppercase tracking-[0.2em] text-brand">404</p>
        <h1 className="mt-3 text-3xl font-black text-slate-950">Page not found</h1>
        <p className="mt-3 text-sm text-slate-600">The route you requested does not exist in the NISF frontend.</p>
        <Button as={Link} className="mt-6" to="/">Back to Dashboard</Button>
      </Card>
    </div>
  );
}
