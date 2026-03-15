import TraceValue from "./TraceValue";
import FindBug from "./FindBug";
import FillBlank from "./FillBlank";
import MatchTypes from "./MatchTypes";
import SortOrder from "./SortOrder";
import MemoryMap from "./MemoryMap";

interface Props {
  challengeType: string;
  payload: Record<string, unknown>;
  onAnswer: (ans: unknown) => void;
  disabled: boolean;
}

export default function ChallengeRouter({ challengeType, payload, onAnswer, disabled }: Props) {
  switch (challengeType) {
    case "trace_value":
      return <TraceValue payload={payload as never} onAnswer={onAnswer as never} disabled={disabled} />;
    case "find_bug":
      return <FindBug payload={payload as never} onAnswer={onAnswer as never} disabled={disabled} />;
    case "fill_blank":
      return <FillBlank payload={payload as never} onAnswer={onAnswer as never} disabled={disabled} />;
    case "match_types":
      return <MatchTypes payload={payload as never} onAnswer={onAnswer as never} disabled={disabled} />;
    case "sort_order":
      return <SortOrder payload={payload as never} onAnswer={onAnswer as never} disabled={disabled} />;
    case "memory_map":
      return <MemoryMap payload={payload as never} onAnswer={onAnswer as never} disabled={disabled} />;
    default:
      return <div className="text-dg-danger">Type de challenge inconnu : {challengeType}</div>;
  }
}
