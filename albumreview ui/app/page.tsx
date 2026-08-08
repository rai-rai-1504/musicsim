"use client";

import { useState, useCallback } from "react";
import { AlbumCreator } from "@/components/album-creator";
import { ReviewsDisplay } from "@/components/reviews-display";
import {
  type Album,
  type AlbumReview,
  CRITICS,
  generateAlbumReview,
} from "@/lib/game-data";
import { Music2, Disc3 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

type GameState = "creating" | "reviewing" | "deluxe";

export default function AlbumReviewGame() {
  const [gameState, setGameState] = useState<GameState>("creating");
  const [currentAlbum, setCurrentAlbum] = useState<Album | null>(null);
  const [reviews, setReviews] = useState<AlbumReview[]>([]);
  const [originalReviews, setOriginalReviews] = useState<AlbumReview[]>([]);
  const [isAnimating, setIsAnimating] = useState(false);

  const handlePublish = useCallback((album: Album) => {
    setCurrentAlbum(album);
    setIsAnimating(true);

    // Generate reviews from all critics
    const newReviews = CRITICS.map((critic) => generateAlbumReview(album, critic));
    
    // Animate transition
    setTimeout(() => {
      setReviews(newReviews);
      setOriginalReviews(newReviews); // Store for deluxe comparison
      setGameState("reviewing");
      setIsAnimating(false);
    }, 1500);
  }, []);

  const handleBack = useCallback(() => {
    setCurrentAlbum(null);
    setReviews([]);
    setGameState("creating");
  }, []);

  const handleCreateDeluxe = useCallback(() => {
    if (currentAlbum) {
      setGameState("deluxe");
    }
  }, [currentAlbum]);

  const handlePublishDeluxe = useCallback((deluxeAlbum: Album) => {
    setCurrentAlbum(deluxeAlbum);
    setIsAnimating(true);

    // Generate reviews from all critics for deluxe, passing original reviews for comparison
    const newReviews = CRITICS.map((critic) => {
      const originalReview = originalReviews.find(r => r.criticId === critic.id);
      return generateAlbumReview(deluxeAlbum, critic, originalReview);
    });
    
    setTimeout(() => {
      setReviews(newReviews);
      setGameState("reviewing");
      setIsAnimating(false);
    }, 1500);
  }, [originalReviews]);

  return (
    <main className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center h-10 w-10 rounded-lg bg-primary text-primary-foreground">
              <Disc3 className="h-6 w-6" />
            </div>
            <div>
              <h1 className="font-bold text-xl">Album Review Simulator</h1>
              <p className="text-xs text-muted-foreground">Create. Publish. Face the critics.</p>
            </div>
          </div>
        </div>
      </header>

      {/* Publishing Animation Overlay */}
      <AnimatePresence>
        {isAnimating && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-background/95 backdrop-blur-sm flex items-center justify-center"
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              className="text-center"
            >
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                className="inline-block mb-6"
              >
                <Disc3 className="h-16 w-16 text-primary" />
              </motion.div>
              <h2 className="text-2xl font-bold mb-2">Sending to Critics...</h2>
              <p className="text-muted-foreground">
                {currentAlbum?.name} is being reviewed by {CRITICS.length} critics
              </p>
              <div className="flex justify-center gap-2 mt-6">
                {CRITICS.map((critic, i) => (
                  <motion.span
                    key={critic.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                    className="text-2xl"
                  >
                    {critic.avatar}
                  </motion.span>
                ))}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <AnimatePresence mode="wait">
          {gameState === "creating" && (
            <motion.div
              key="creating"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <div className="max-w-5xl mx-auto">
                <div className="text-center mb-8">
                  <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-muted text-sm mb-4">
                    <Music2 className="h-4 w-4" />
                    <span>Album Creation Mode</span>
                  </div>
                  <h2 className="text-3xl font-bold mb-2">Create Your Album</h2>
                  <p className="text-muted-foreground max-w-md mx-auto">
                    Generate songs, arrange your tracklist, and publish to see what the critics think.
                    Minimum 7 songs required.
                  </p>
                </div>
                <AlbumCreator onPublish={handlePublish} />
              </div>
            </motion.div>
          )}

          {gameState === "reviewing" && currentAlbum && (
            <motion.div
              key="reviewing"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <div className="max-w-5xl mx-auto">
                <ReviewsDisplay
                  album={currentAlbum}
                  reviews={reviews}
                  onBack={handleBack}
                  onCreateDeluxe={handleCreateDeluxe}
                />
              </div>
            </motion.div>
          )}

          {gameState === "deluxe" && currentAlbum && (
            <motion.div
              key="deluxe"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <div className="max-w-5xl mx-auto">
                <div className="text-center mb-8">
                  <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-amber-500/20 to-yellow-500/20 text-amber-600 dark:text-amber-400 text-sm mb-4 border border-amber-500/30">
                    <Disc3 className="h-4 w-4" />
                    <span>Deluxe Edition Mode</span>
                  </div>
                  <h2 className="text-3xl font-bold mb-2">Create Deluxe Edition</h2>
                  <p className="text-muted-foreground max-w-md mx-auto">
                    Add bonus tracks, reorder songs, and publish the deluxe version of &quot;{currentAlbum.name}&quot;.
                    Critics will review the whole album fresh.
                  </p>
                </div>
                <AlbumCreator
                  onPublish={handlePublishDeluxe}
                  existingAlbum={{
                    ...currentAlbum,
                    name: `${currentAlbum.name} (Deluxe)`,
                  }}
                />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Footer */}
      <footer className="border-t border-border mt-auto">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
          <p>Create albums, face the critics, chase the perfect score.</p>
        </div>
      </footer>
    </main>
  );
}
