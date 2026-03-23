import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

type VideoAdProps = {
  title: string;
  subtitle: string;
  ctaText: string;
  backgroundColor: string;
  accentColor: string;
};

export const VideoAd: React.FC<VideoAdProps> = ({
  title,
  subtitle,
  ctaText,
  backgroundColor,
  accentColor,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Title slides up and fades in
  const titleProgress = spring({
    frame,
    fps,
    from: 0,
    to: 1,
    config: { damping: 12, stiffness: 80 },
  });

  // Subtitle appears after title
  const subtitleProgress = spring({
    frame: frame - 15,
    fps,
    from: 0,
    to: 1,
    config: { damping: 12, stiffness: 80 },
  });

  // CTA button appears last
  const ctaProgress = spring({
    frame: frame - 40,
    fps,
    from: 0,
    to: 1,
    config: { damping: 10, stiffness: 60 },
  });

  // Background pulse
  const bgOpacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "'Arial', sans-serif",
        opacity: bgOpacity,
      }}
    >
      {/* Decorative accent bar */}
      <div
        style={{
          width: `${interpolate(titleProgress, [0, 1], [0, 200])}px`,
          height: 4,
          backgroundColor: accentColor,
          marginBottom: 40,
          borderRadius: 2,
        }}
      />

      {/* Title */}
      <h1
        style={{
          fontSize: 96,
          fontWeight: 900,
          color: "#ffffff",
          margin: 0,
          textAlign: "center",
          letterSpacing: "-2px",
          opacity: titleProgress,
          transform: `translateY(${interpolate(titleProgress, [0, 1], [60, 0])}px)`,
        }}
      >
        {title}
      </h1>

      {/* Subtitle */}
      <p
        style={{
          fontSize: 40,
          color: "#94a3b8",
          marginTop: 24,
          textAlign: "center",
          maxWidth: 1000,
          lineHeight: 1.4,
          opacity: subtitleProgress,
          transform: `translateY(${interpolate(subtitleProgress, [0, 1], [40, 0])}px)`,
        }}
      >
        {subtitle}
      </p>

      {/* CTA Button */}
      <div
        style={{
          marginTop: 64,
          backgroundColor: accentColor,
          paddingTop: 24,
          paddingBottom: 24,
          paddingLeft: 56,
          paddingRight: 56,
          borderRadius: 12,
          opacity: ctaProgress,
          transform: `scale(${interpolate(ctaProgress, [0, 1], [0.8, 1])})`,
        }}
      >
        <span
          style={{
            fontSize: 36,
            fontWeight: 700,
            color: "#ffffff",
            letterSpacing: "0.5px",
          }}
        >
          {ctaText}
        </span>
      </div>
    </AbsoluteFill>
  );
};
