import Badge from "../common/Badge";
import { statusClass, statusLabel } from "../../utils/statusFormatter";

export default function JobStatusBadge({ status }) {
  return <Badge className={statusClass(status)}>{statusLabel(status)}</Badge>;
}
