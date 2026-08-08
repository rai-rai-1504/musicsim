"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  CRITICS,
  type Album,
  type AlbumReview,
  calculateAggregateScore,
  getConsensusLabel,
  getScoreColor,
  getScoreBgColor,
  formatDuration,
} from "@/lib/game-data";
import { Star, Music, ArrowLeft, Sparkles, Trophy, AlertTriangle, ArrowUp, ArrowDown, Minus } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface CriticCardProps {
  review: AlbumReview;
  onClick: () => void;
  index: number;
}

function CriticCard({ review, onClick, index }: CriticCardProps) {
  const critic = CRITICS.find((c) => c.id === review.criticId)!;
  const scoreColor = getScoreColor(review.albumScore);
  const scoreBg = getScoreBgColor(review.albumScore);
  
  // Calculate score change for deluxe editions
  const hasOriginalScore = review.originalScore !== undefined;
  const scoreDiff = hasOriginalScore ? review.albumScore - review.originalScore! : 0;
  const improved = scoreDiff > 0.3;
  const declined = scoreDiff < -0.3;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
    >
      <Card
        className="cursor-pointer group hover:shadow-lg transition-all duration-300 hover:scale-[1.02] overflow-hidden"
        onClick={onClick}
      >
        <div className={`h-2 bg-gradient-to-r ${critic.color}`} />
        <CardContent className="p-5">
          <div className="flex items-start gap-4">
            <div className="text-4xl">{critic.avatar}</div>
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-lg">{critic.name}</h3>
              <p className="text-sm text-muted-foreground truncate">{critic.tagline}</p>
            </div>
            <div className="text-right">
              <div
                className={`text-3xl font-bold tabular-nums ${scoreColor}`}
              >
                {review.albumScore}
              </div>
              <div className="text-xs text-muted-foreground">/10</div>
              {hasOriginalScore && (
                <div className={`flex items-center justify-end gap-1 mt-1 text-xs ${
                  improved ? "text-emerald-500" : declined ? "text-red-500" : "text-muted-foreground"
                }`}>
                  {improved ? <ArrowUp className="h-3 w-3" /> : declined ? <ArrowDown className="h-3 w-3" /> : <Minus className="h-3 w-3" />}
                  <span>from {review.originalScore}</span>
                </div>
              )}
            </div>
          </div>
          <div className="mt-4 pt-4 border-t border-border">
            <p className="text-sm text-muted-foreground line-clamp-2 italic">
              &quot;{review.verdict}&quot;
            </p>
          </div>
          <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
            <span>Click to read full review</span>
            <div className={`h-2 w-2 rounded-full ${scoreBg}`} />
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

interface FullReviewModalProps {
  review: AlbumReview;
  album: Album;
  onClose: () => void;
}

function FullReviewModal({ review, album, onClose }: FullReviewModalProps) {
  const critic = CRITICS.find((c) => c.id === review.criticId)!;
  const scoreColor = getScoreColor(review.albumScore);

  const bestSong = review.songReviews.reduce((best, curr) =>
    curr.score > best.score ? curr : best
  );
  const worstSong = review.songReviews.reduce((worst, curr) =>
    curr.score < worst.score ? curr : worst
  );

  return (
    <DialogContent className="max-w-2xl max-h-[90vh] p-0 overflow-hidden">
      <div className={`h-3 bg-gradient-to-r ${critic.color}`} />
      <ScrollArea className="max-h-[calc(90vh-3rem)]">
        <div className="p-6">
          <DialogHeader>
            <div className="flex items-start gap-4">
              <div className="text-5xl">{critic.avatar}</div>
              <div className="flex-1">
                <DialogTitle className="text-2xl">{critic.name}</DialogTitle>
                <DialogDescription>{critic.tagline}</DialogDescription>
              </div>
              <div className="text-right">
                <div className={`text-4xl font-bold tabular-nums ${scoreColor}`}>
                  {review.albumScore}
                </div>
                <div className="text-sm text-muted-foreground">/10</div>
                {review.originalScore !== undefined && (
                  <div className={`flex items-center justify-end gap-1 mt-1 text-sm ${
                    review.albumScore > review.originalScore + 0.3 
                      ? "text-emerald-500" 
                      : review.albumScore < review.originalScore - 0.3 
                        ? "text-red-500" 
                        : "text-muted-foreground"
                  }`}>
                    {review.albumScore > review.originalScore + 0.3 
                      ? <ArrowUp className="h-4 w-4" /> 
                      : review.albumScore < review.originalScore - 0.3 
                        ? <ArrowDown className="h-4 w-4" /> 
                        : <Minus className="h-4 w-4" />
                    }
                    <span>Previously: {review.originalScore}/10</span>
                  </div>
                )}
              </div>
            </div>
          </DialogHeader>

          <div className="mt-6 space-y-6">
            {/* Album Info */}
            <div className="flex items-center gap-3 text-sm text-muted-foreground">
              <Music className="h-4 w-4" />
              <span className="font-medium text-foreground">{album.name}</span>
              <span>•</span>
              <span>{album.songs.length} tracks</span>
              <span>•</span>
              <span>{formatDuration(album.songs.reduce((s, song) => s + song.duration, 0))}</span>
              {album.isDeluxe && (
                <Badge variant="secondary" className="ml-2">Deluxe</Badge>
              )}
            </div>

            {/* Full Review */}
            <div className="p-4 rounded-lg bg-muted/50 border">
              <p className="text-foreground leading-relaxed">{review.fullReview}</p>
            </div>

{/* Deluxe Comparison - if available */}
            {album.isDeluxe && review.deluxeComparison && (
              <div className={`p-4 rounded-lg border ${
                review.albumScore > (review.originalScore || 0) + 0.3
                  ? "bg-emerald-500/10 border-emerald-500/30"
                  : review.albumScore < (review.originalScore || 0) - 0.3
                    ? "bg-red-500/10 border-red-500/30"
                    : "bg-muted/50 border-border"
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  <Badge variant="secondary" className="text-xs">Deluxe Edition Comparison</Badge>
                  {review.originalScore !== undefined && (
                    <span className="text-xs text-muted-foreground">
                      Standard Edition: {review.originalScore}/10
                    </span>
                  )}
                </div>
                <p className="text-sm text-foreground leading-relaxed italic">
                  {review.deluxeComparison}
                </p>
              </div>
            )}

            {/* Verdict */}
            <div className="p-4 rounded-lg bg-gradient-to-br from-primary/10 to-primary/5 border border-primary/20">
              <div className="flex items-start gap-3">
                <Sparkles className="h-5 w-5 text-primary mt-0.5" />
                <p className="italic text-foreground">&quot;{review.verdict}&quot;</p>
              </div>
            </div>

            {/* Best & Worst */}
            <div className="grid sm:grid-cols-2 gap-4">
              <div className="p-4 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                <div className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400 mb-2">
                  <Trophy className="h-4 w-4" />
                  <span className="font-medium text-sm">Standout Track</span>
                </div>
                <p className="font-medium">{bestSong.songName}</p>
                <p className="text-sm text-muted-foreground">{bestSong.score}/10</p>
              </div>
              <div className="p-4 rounded-lg bg-orange-500/10 border border-orange-500/20">
                <div className="flex items-center gap-2 text-orange-600 dark:text-orange-400 mb-2">
                  <AlertTriangle className="h-4 w-4" />
                  <span className="font-medium text-sm">Weakest Moment</span>
                </div>
                <p className="font-medium">{worstSong.songName}</p>
                <p className="text-sm text-muted-foreground">{worstSong.score}/10</p>
              </div>
            </div>

            {/* Track Ratings */}
            <div>
              <h4 className="font-semibold mb-3">Track-by-Track Ratings</h4>
              <div className="space-y-3">
                {review.songReviews.map((songReview, idx) => {
                  const song = album.songs.find((s) => s.id === songReview.songId);
                  const scorePercent = (songReview.score / 10) * 100;
                  return (
                    <div key={songReview.songId} className="space-y-1">
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-2">
                          <span className="text-muted-foreground font-mono w-6">
                            {String(idx + 1).padStart(2, "0")}
                          </span>
                          <span className="font-medium">{songReview.songName}</span>
                        </div>
                        <span className={`font-bold tabular-nums ${getScoreColor(songReview.score)}`}>
                          {songReview.score}
                        </span>
                      </div>
                      <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                        <div
                          className={`h-full transition-all duration-500 rounded-full ${getScoreBgColor(songReview.score)}`}
                          style={{ width: `${scorePercent}%` }}
                        />
                      </div>
                      <p className="text-xs text-muted-foreground pl-8 italic">
                        {songReview.comment}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </ScrollArea>
    </DialogContent>
  );
}

interface ReviewsDisplayProps {
  album: Album;
  reviews: AlbumReview[];
  onBack: () => void;
  onCreateDeluxe: () => void;
}

export function ReviewsDisplay({
  album,
  reviews,
  onBack,
  onCreateDeluxe,
}: ReviewsDisplayProps) {
  const [selectedReview, setSelectedReview] = useState<AlbumReview | null>(null);

  const avgScore = calculateAggregateScore(reviews);
  const consensus = getConsensusLabel(avgScore);
  const scoreColor = getScoreColor(avgScore);

  // Get aggregate track scores
  const aggregateTrackScores = album.songs.map((song) => {
    const scores = reviews.map((r) => {
      const sr = r.songReviews.find((s) => s.songId === song.id);
      return sr?.score || 0;
    });
    return {
      song,
      avgScore: Math.round((scores.reduce((a, b) => a + b, 0) / scores.length) * 10) / 10,
    };
  });

  const bestTrack = aggregateTrackScores.reduce((best, curr) =>
    curr.avgScore > best.avgScore ? curr : best
  );
  const worstTrack = aggregateTrackScores.reduce((worst, curr) =>
    curr.avgScore < worst.avgScore ? curr : worst
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={onBack}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">{album.name}</h1>
          <p className="text-muted-foreground capitalize">
            {album.coreGenre} • {album.coreTheme} • {album.songs.length} tracks
            {album.isDeluxe && <Badge variant="secondary" className="ml-2">Deluxe</Badge>}
          </p>
        </div>
      </div>

      {/* Aggregate Score */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
      >
        <Card className="bg-gradient-to-br from-card to-muted/30 border-2">
          <CardContent className="p-6">
            <div className="flex flex-col sm:flex-row items-center gap-6">
              <div className="text-center">
                <div className={`text-6xl font-bold tabular-nums ${scoreColor}`}>
                  {avgScore}
                </div>
                <div className="text-muted-foreground">/10 Average</div>
              </div>
              <div className="h-16 w-px bg-border hidden sm:block" />
              <div className="flex-1 text-center sm:text-left">
                <div className="flex items-center justify-center sm:justify-start gap-2 mb-2">
                  {avgScore >= 9 && <Star className="h-5 w-5 text-yellow-500 fill-yellow-500" />}
                  <span className="font-semibold text-lg">{consensus}</span>
                  {avgScore >= 9 && <Star className="h-5 w-5 text-yellow-500 fill-yellow-500" />}
                </div>
                <p className="text-sm text-muted-foreground">
                  Based on {reviews.length} critic reviews
                </p>
              </div>
              <div className="flex flex-col gap-2">
                <div className="text-center sm:text-right text-sm">
                  <div className="flex items-center gap-2 text-emerald-500">
                    <Trophy className="h-4 w-4" />
                    <span>Best: {bestTrack.song.name} ({bestTrack.avgScore})</span>
                  </div>
                  <div className="flex items-center gap-2 text-orange-500">
                    <AlertTriangle className="h-4 w-4" />
                    <span>Weakest: {worstTrack.song.name} ({worstTrack.avgScore})</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Actions */}
      <div className="flex gap-3">
        <Button variant="outline" onClick={onBack}>
          Create Another Album
        </Button>
        {!album.isDeluxe && (
          <Button onClick={onCreateDeluxe}>
            <Sparkles className="h-4 w-4 mr-2" />
            Create Deluxe Edition
          </Button>
        )}
      </div>

      {/* Critic Cards */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Critic Reviews</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {reviews.map((review, idx) => (
            <CriticCard
              key={review.criticId}
              review={review}
              onClick={() => setSelectedReview(review)}
              index={idx}
            />
          ))}
        </div>
      </div>

      {/* Aggregate Track Scores */}
      <Card>
        <CardContent className="p-6">
          <h3 className="font-semibold mb-4">Aggregate Track Scores</h3>
          <div className="space-y-3">
            {aggregateTrackScores.map((item, idx) => {
              const scorePercent = (item.avgScore / 10) * 100;
              return (
                <div key={item.song.id} className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2">
                      <span className="text-muted-foreground font-mono w-6">
                        {String(idx + 1).padStart(2, "0")}
                      </span>
                      <span className="font-medium">{item.song.name}</span>
                      <span className="text-xs text-muted-foreground capitalize">
                        ({item.song.genres.join("/")})
                      </span>
                    </div>
                    <span className={`font-bold tabular-nums ${getScoreColor(item.avgScore)}`}>
                      {item.avgScore}
                    </span>
                  </div>
                  <div className="h-2 bg-muted rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${scorePercent}%` }}
                      transition={{ delay: idx * 0.05, duration: 0.5 }}
                      className={`h-full rounded-full ${getScoreBgColor(item.avgScore)}`}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Full Review Modal */}
      <Dialog open={!!selectedReview} onOpenChange={() => setSelectedReview(null)}>
        <AnimatePresence>
          {selectedReview && (
            <FullReviewModal
              review={selectedReview}
              album={album}
              onClose={() => setSelectedReview(null)}
            />
          )}
        </AnimatePresence>
      </Dialog>
    </div>
  );
}
