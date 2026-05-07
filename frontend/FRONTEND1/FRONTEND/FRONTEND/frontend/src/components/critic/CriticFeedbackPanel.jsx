import EmptyState from "../common/EmptyState";
import CriticDirectiveCard from "./CriticDirectiveCard";

export default function CriticFeedbackPanel({ directives = [] }) {
  if (!directives.length) return <EmptyState title="No Critic Feedback" message="No critic feedback available." />;
  return <div className="grid gap-3">{directives.map((directive, index) => <CriticDirectiveCard key={`${directive.target_dimension}-${index}`} directive={directive} />)}</div>;
}
