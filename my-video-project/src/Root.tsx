import { Composition } from "remotion";
import { VideoAd } from "./VideoAd";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="VideoAd"
        component={VideoAd}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Your Product",
          subtitle: "The best solution for your needs",
          ctaText: "Get Started Today",
          backgroundColor: "#0f172a",
          accentColor: "#6366f1",
        }}
      />
    </>
  );
};
