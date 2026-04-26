export interface WebUser {
  id: string
  email: string
  name: string
  line_user_id: string | null
}

export interface Group {
  id: string
  name: string
  description?: string
  member_count?: number
}

export interface UserGroup {
  group: Group
  joined_at?: string
}

export interface Match {
  id: string
  group_id: string
  date: string
  hanchan_count: number
  is_deleted: boolean
}

export interface Hanchan {
  id: string
  match_id: string
  date: string
  scores: PlayerScore[]
}

export interface PlayerScore {
  user_id: string
  user_name: string
  score: number
  rank: number
  point: number
}

export interface RankingEntry {
  rank: number
  user_id: string
  user_name: string
  total_point: number
  hanchan_count: number
  average_rank: number
  first_count: number
  second_count: number
  third_count: number
  fourth_count: number
}

export interface GroupStats {
  point_history: PointHistoryEntry[]
  rank_distribution: RankDistributionEntry[]
}

export interface PointHistoryEntry {
  date: string
  [user_name: string]: string | number
}

export interface RankDistributionEntry {
  user_name: string
  first: number
  second: number
  third: number
  fourth: number
}

export interface UserStats {
  total_hanchan: number
  total_point: number
  average_rank: number
  rank_distribution: {
    first: number
    second: number
    third: number
    fourth: number
  }
  point_history: PointHistoryEntry[]
}
