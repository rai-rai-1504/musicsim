"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import {
  GENRES,
  THEMES,
  QUALITY_FLAVORS,
  MIN_SONGS,
  generateSongQuality,
  generateId,
  formatDuration,
  pick,
  type Song,
  type Album,
  type Genre,
  type Theme,
} from "@/lib/game-data";
import { GripVertical, Music, Trash2, Plus, Sparkles, Send, Star, Shuffle, Check, Info, Disc3, HelpCircle } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface SortableSongProps {
  song: Song;
  index: number;
  onRemove: (id: string) => void;
  isDeluxeTrack?: boolean;
}

function SortableSong({ song, index, onRemove, isDeluxeTrack }: SortableSongProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: song.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  const qualityColor = song.quality >= 8 
    ? "text-emerald-500" 
    : song.quality >= 5 
      ? "text-yellow-500" 
      : "text-red-500";

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`flex items-center gap-3 p-3 bg-card border rounded-lg group transition-all ${
        isDragging ? "opacity-50 shadow-lg border-primary" : "border-border hover:border-muted-foreground/50"
      } ${isDeluxeTrack ? "bg-amber-500/5 border-amber-500/30" : ""}`}
    >
      <button
        {...attributes}
        {...listeners}
        className="cursor-grab active:cursor-grabbing text-muted-foreground hover:text-foreground transition-colors touch-none"
        aria-label="Drag to reorder"
      >
        <GripVertical className="h-5 w-5" />
      </button>
      <span className="text-muted-foreground font-mono text-sm w-6">
        {String(index + 1).padStart(2, "0")}
      </span>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <p className="font-medium truncate">{song.name}</p>
          {isDeluxeTrack && (
            <Badge variant="outline" className="text-xs text-amber-500 border-amber-500/50">
              Bonus
            </Badge>
          )}
        </div>
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span className="capitalize">
            {song.genres.join(" / ")}
          </span>
          <span>•</span>
          <span className="capitalize">{song.theme}</span>
          <span>•</span>
          <span>{formatDuration(song.duration)}</span>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <Badge
                variant="outline"
                className={`font-mono cursor-help ${qualityColor} border-current/30`}
              >
                Q{song.quality}
              </Badge>
            </TooltipTrigger>
            <TooltipContent>
              <p>Song Quality: {song.quality}/10</p>
              <p className="text-xs text-muted-foreground">Higher quality improves critic scores</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity text-destructive hover:text-destructive hover:bg-destructive/10"
          onClick={() => onRemove(song.id)}
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}

interface AlbumCreatorProps {
  onPublish: (album: Album) => void;
  existingAlbum?: Album;
}

export function AlbumCreator({ onPublish, existingAlbum }: AlbumCreatorProps) {
  const [albumName, setAlbumName] = useState(existingAlbum?.name || "");
  const [coreGenre, setCoreGenre] = useState<Genre | "">(existingAlbum?.coreGenre || "");
  const [coreTheme, setCoreTheme] = useState<Theme | "">(existingAlbum?.coreTheme || "");
  const [songs, setSongs] = useState<Song[]>(existingAlbum?.songs || []);
  const [isCreatingAlbum, setIsCreatingAlbum] = useState(!existingAlbum);
  const [originalSongCount] = useState(existingAlbum?.songs.length || 0);
  
  // Song creation state
  const [currentQuality, setCurrentQuality] = useState<number | null>(null);
  const [currentFlavor, setCurrentFlavor] = useState("");
  const [songName, setSongName] = useState("");
  const [songGenres, setSongGenres] = useState<Genre[]>([]);
  const [songTheme, setSongTheme] = useState<Theme | "">("");
  const [songMinutes, setSongMinutes] = useState("3");
  const [songSeconds, setSongSeconds] = useState("30");
  const [isAddingSong, setIsAddingSong] = useState(false);
  const [activeTab, setActiveTab] = useState("tracklist");

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (over && active.id !== over.id) {
      setSongs((items) => {
        const oldIndex = items.findIndex((i) => i.id === active.id);
        const newIndex = items.findIndex((i) => i.id === over.id);
        return arrayMove(items, oldIndex, newIndex);
      });
    }
  };

  const generateNewSong = useCallback(() => {
    const quality = generateSongQuality();
    const flavor = pick(QUALITY_FLAVORS);
    setCurrentQuality(quality);
    setCurrentFlavor(flavor);
    setSongName("");
    setSongGenres(coreGenre ? [coreGenre] : []);
    setSongTheme(coreTheme || "");
    setSongMinutes("3");
    setSongSeconds("30");
    setIsAddingSong(true);
    setActiveTab("studio");
  }, [coreGenre, coreTheme]);

  const handleCreateAlbum = () => {
    if (albumName && coreGenre && coreTheme) {
      setIsCreatingAlbum(false);
    }
  };

  const handleAddSong = () => {
    if (currentQuality && songName && songGenres.length > 0 && songTheme) {
      const duration = parseInt(songMinutes) * 60 + parseInt(songSeconds);
      const newSong: Song = {
        id: generateId(),
        name: songName,
        quality: currentQuality,
        genres: songGenres,
        theme: songTheme as Theme,
        duration,
      };
      setSongs([...songs, newSong]);
      setCurrentQuality(null);
      setIsAddingSong(false);
      setActiveTab("tracklist");
    }
  };

  const handleRemoveSong = (id: string) => {
    setSongs(songs.filter((s) => s.id !== id));
  };

  const handlePublish = () => {
    if (songs.length >= MIN_SONGS && albumName && coreGenre && coreTheme) {
      const album: Album = {
        id: generateId(),
        name: albumName,
        coreGenre: coreGenre as Genre,
        coreTheme: coreTheme as Theme,
        songs,
        isDeluxe: !!existingAlbum,
        originalAlbumId: existingAlbum?.id,
      };
      onPublish(album);
    }
  };

  const toggleGenre = (genre: Genre) => {
    if (songGenres.includes(genre)) {
      setSongGenres(songGenres.filter((g) => g !== genre));
    } else if (songGenres.length < 2) {
      setSongGenres([...songGenres, genre]);
    }
  };

  const totalDuration = songs.reduce((sum, s) => sum + s.duration, 0);
  const avgQuality = songs.length > 0
    ? Math.round((songs.reduce((sum, s) => sum + s.quality, 0) / songs.length) * 10) / 10
    : 0;

  const canPublish = songs.length >= MIN_SONGS && albumName && coreGenre && coreTheme;

  if (isCreatingAlbum) {
    return (
      <Card className="max-w-lg mx-auto">
        <CardHeader className="space-y-1">
          <CardTitle className="flex items-center gap-2">
            {existingAlbum ? (
              <>
                <Sparkles className="h-5 w-5 text-amber-500" />
                Create Deluxe Edition
              </>
            ) : (
              <>
                <Disc3 className="h-5 w-5 text-primary" />
                Create New Album
              </>
            )}
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            {existingAlbum 
              ? "Expand your album with bonus tracks for a fresh review."
              : "Define your album's identity before adding songs."
            }
          </p>
        </CardHeader>
        <CardContent className="space-y-5">
          <div className="space-y-2">
            <Label htmlFor="albumName">Album Name</Label>
            <Input
              id="albumName"
              placeholder="Enter a memorable album title..."
              value={albumName}
              onChange={(e) => setAlbumName(e.target.value)}
              className="text-lg"
            />
          </div>
          
          <div className="grid sm:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="coreGenre">Core Genre</Label>
              <Select value={coreGenre} onValueChange={(v) => setCoreGenre(v as Genre)}>
                <SelectTrigger id="coreGenre">
                  <SelectValue placeholder="Select genre..." />
                </SelectTrigger>
                <SelectContent>
                  {GENRES.map((g) => (
                    <SelectItem key={g} value={g} className="capitalize">
                      {g}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground">
                Songs matching your core genre score better
              </p>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="coreTheme">Core Theme</Label>
              <Select value={coreTheme} onValueChange={(v) => setCoreTheme(v as Theme)}>
                <SelectTrigger id="coreTheme">
                  <SelectValue placeholder="Select theme..." />
                </SelectTrigger>
                <SelectContent>
                  {THEMES.map((t) => (
                    <SelectItem key={t} value={t} className="capitalize">
                      {t}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground">
                Thematic consistency improves reviews
              </p>
            </div>
          </div>

          <div className="pt-2">
            <Button
              className="w-full"
              size="lg"
              onClick={handleCreateAlbum}
              disabled={!albumName || !coreGenre || !coreTheme}
            >
              <Check className="h-4 w-4 mr-2" />
              Start Creating Songs
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Album Header */}
      <Card>
        <CardContent className="p-4 sm:p-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className={`h-16 w-16 rounded-lg flex items-center justify-center text-3xl ${
                existingAlbum ? "bg-gradient-to-br from-amber-500/20 to-yellow-500/20" : "bg-gradient-to-br from-primary/20 to-primary/10"
              }`}>
                {existingAlbum ? <Sparkles className="h-8 w-8 text-amber-500" /> : <Disc3 className="h-8 w-8 text-primary" />}
              </div>
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">{albumName}</h2>
                <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
                  <Badge variant="outline" className="capitalize">{coreGenre}</Badge>
                  <Badge variant="outline" className="capitalize">{coreTheme}</Badge>
                  {existingAlbum && (
                    <Badge className="bg-amber-500/20 text-amber-500 border-amber-500/30">
                      Deluxe Edition
                    </Badge>
                  )}
                </div>
              </div>
            </div>
            <div className="flex items-center gap-6 text-sm">
              <div className="text-center">
                <div className="text-2xl font-bold">{songs.length}</div>
                <div className="text-muted-foreground">Tracks</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">{formatDuration(totalDuration)}</div>
                <div className="text-muted-foreground">Duration</div>
              </div>
              <div className="text-center">
                <div className={`text-2xl font-bold ${avgQuality >= 7 ? "text-emerald-500" : avgQuality >= 4 ? "text-yellow-500" : "text-red-500"}`}>
                  {avgQuality || "—"}
                </div>
                <div className="text-muted-foreground">Avg Quality</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <TabsList>
            <TabsTrigger value="tracklist" className="gap-2">
              <Music className="h-4 w-4" />
              Tracklist
            </TabsTrigger>
            <TabsTrigger value="studio" className="gap-2" disabled={!isAddingSong && !currentQuality}>
              <Sparkles className="h-4 w-4" />
              Song Studio
            </TabsTrigger>
          </TabsList>
          
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={generateNewSong}
            >
              <Plus className="h-4 w-4 mr-2" />
              Add Song
            </Button>
            <Button
              onClick={handlePublish}
              disabled={!canPublish}
              className={canPublish ? "bg-primary" : ""}
            >
              <Send className="h-4 w-4 mr-2" />
              Publish ({songs.length}/{MIN_SONGS})
            </Button>
          </div>
        </div>

        <TabsContent value="tracklist" className="mt-0">
          <Card>
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg flex items-center gap-2">
                  Tracklist
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <HelpCircle className="h-4 w-4 text-muted-foreground cursor-help" />
                      </TooltipTrigger>
                      <TooltipContent className="max-w-xs">
                        <p className="font-medium mb-1">Tips for better reviews:</p>
                        <ul className="text-xs space-y-1 text-muted-foreground">
                          <li>• Drag songs to reorder — track flow affects scores</li>
                          <li>• Songs matching your core genre score higher</li>
                          <li>• Consistent themes improve cohesion ratings</li>
                          <li>• Different critics have different preferences</li>
                        </ul>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </CardTitle>
                {songs.length > 0 && (
                  <span className="text-sm text-muted-foreground">
                    Drag to reorder
                  </span>
                )}
              </div>
            </CardHeader>
            <CardContent>
              {songs.length === 0 ? (
                <div className="text-center py-12 text-muted-foreground border-2 border-dashed border-border rounded-lg">
                  <Music className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p className="font-medium">No tracks yet</p>
                  <p className="text-sm mt-1">
                    Generate your first song to start building your album.
                  </p>
                  <p className="text-xs mt-2 text-muted-foreground/70">
                    Minimum {MIN_SONGS} songs required to publish.
                  </p>
                  <Button className="mt-4" onClick={generateNewSong}>
                    <Plus className="h-4 w-4 mr-2" />
                    Generate First Song
                  </Button>
                </div>
              ) : (
                <DndContext
                  sensors={sensors}
                  collisionDetection={closestCenter}
                  onDragEnd={handleDragEnd}
                >
                  <SortableContext
                    items={songs.map((s) => s.id)}
                    strategy={verticalListSortingStrategy}
                  >
                    <div className="space-y-2">
                      {songs.map((song, index) => (
                        <SortableSong
                          key={song.id}
                          song={song}
                          index={index}
                          onRemove={handleRemoveSong}
                          isDeluxeTrack={existingAlbum && index >= originalSongCount}
                        />
                      ))}
                    </div>
                  </SortableContext>
                </DndContext>
              )}

              {songs.length > 0 && songs.length < MIN_SONGS && (
                <div className="mt-4 p-3 bg-muted/50 rounded-lg border border-border">
                  <p className="text-sm text-muted-foreground flex items-center gap-2">
                    <Info className="h-4 w-4" />
                    Add {MIN_SONGS - songs.length} more song{MIN_SONGS - songs.length !== 1 ? "s" : ""} to publish your album.
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="studio" className="mt-0">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-primary" />
                Song Studio
              </CardTitle>
            </CardHeader>
            <CardContent>
              {!isAddingSong || !currentQuality ? (
                <div className="text-center py-12 text-muted-foreground">
                  <Sparkles className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p className="font-medium">Ready to create</p>
                  <p className="text-sm mt-1">
                    Click &quot;Add Song&quot; to generate a new track.
                  </p>
                  <Button className="mt-4" onClick={generateNewSong}>
                    <Plus className="h-4 w-4 mr-2" />
                    Generate New Song
                  </Button>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Quality Display */}
                  <div className="p-5 rounded-xl bg-gradient-to-br from-primary/10 via-primary/5 to-transparent border border-primary/20">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <span className="text-sm font-medium text-muted-foreground">Song Quality</span>
                        <p className="text-sm text-muted-foreground/70 italic mt-1">&quot;{currentFlavor}&quot;</p>
                      </div>
                      <div className={`text-4xl font-bold ${
                        currentQuality >= 8 ? "text-emerald-500" : 
                        currentQuality >= 5 ? "text-yellow-500" : "text-red-500"
                      }`}>
                        {currentQuality}<span className="text-lg text-muted-foreground">/10</span>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={generateNewSong}
                        className="flex-1"
                      >
                        <Shuffle className="h-4 w-4 mr-2" />
                        Re-roll Quality
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          setIsAddingSong(false);
                          setCurrentQuality(null);
                          setActiveTab("tracklist");
                        }}
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>

                  {/* Song Details Form */}
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="songName">Song Name</Label>
                      <Input
                        id="songName"
                        placeholder="Enter a song title..."
                        value={songName}
                        onChange={(e) => setSongName(e.target.value)}
                        className="text-lg"
                      />
                    </div>

                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <Label>Genre(s)</Label>
                        <span className="text-xs text-muted-foreground">Select 1-2 genres</span>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {GENRES.map((g) => {
                          const isSelected = songGenres.includes(g);
                          const isCore = g === coreGenre;
                          return (
                            <Badge
                              key={g}
                              variant={isSelected ? "default" : "outline"}
                              className={`cursor-pointer capitalize transition-all ${
                                isSelected 
                                  ? "bg-primary text-primary-foreground" 
                                  : isCore 
                                    ? "border-primary/50 text-primary hover:bg-primary/10" 
                                    : "hover:bg-muted"
                              }`}
                              onClick={() => toggleGenre(g)}
                            >
                              {isCore && !isSelected && <Star className="h-3 w-3 mr-1" />}
                              {g}
                            </Badge>
                          );
                        })}
                      </div>
                    </div>

                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <Label htmlFor="songTheme">Theme</Label>
                        {coreTheme && (
                          <span className="text-xs text-muted-foreground flex items-center gap-1">
                            <Star className="h-3 w-3" /> Core: {coreTheme}
                          </span>
                        )}
                      </div>
                      <Select value={songTheme} onValueChange={(v) => setSongTheme(v as Theme)}>
                        <SelectTrigger id="songTheme">
                          <SelectValue placeholder="Select theme..." />
                        </SelectTrigger>
                        <SelectContent>
                          {THEMES.map((t) => (
                            <SelectItem key={t} value={t} className="capitalize">
                              {t === coreTheme && <Star className="h-3 w-3 inline mr-2" />}
                              {t}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label>Duration</Label>
                      <div className="flex items-center gap-2">
                        <div className="flex-1">
                          <Input
                            type="number"
                            min="0"
                            max="15"
                            value={songMinutes}
                            onChange={(e) => setSongMinutes(e.target.value)}
                            className="text-center"
                          />
                          <span className="text-xs text-muted-foreground text-center block mt-1">Minutes</span>
                        </div>
                        <span className="text-xl text-muted-foreground pb-5">:</span>
                        <div className="flex-1">
                          <Input
                            type="number"
                            min="0"
                            max="59"
                            value={songSeconds}
                            onChange={(e) => setSongSeconds(e.target.value)}
                            className="text-center"
                          />
                          <span className="text-xs text-muted-foreground text-center block mt-1">Seconds</span>
                        </div>
                      </div>
                    </div>

                    <Button
                      className="w-full"
                      size="lg"
                      onClick={handleAddSong}
                      disabled={!songName || songGenres.length === 0 || !songTheme}
                    >
                      <Check className="h-4 w-4 mr-2" />
                      Add to Album
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
