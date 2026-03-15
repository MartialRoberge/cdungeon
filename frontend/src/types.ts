export interface BadgeOut {
  id: string;
  name: string;
  description: string;
  icon_key: string;
  category: string;
  secret: boolean;
  earned: boolean;
  earned_at: string | null;
}
