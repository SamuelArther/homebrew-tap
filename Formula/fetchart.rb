class Fetchart < Formula
  desc "Download game art, achievements, posters, album covers and more from the command line"
  homepage "https://github.com/SamuelArther/fetchart"
  url "https://github.com/SamuelArther/fetchart/releases/download/v1.5.0/fetchart-windows.exe"
  sha256 "0782758399782cd548e2987ec326920aae6f756eff5c9690a8ee305a7a6c349f"
  license "MIT"

  # The standalone Windows build from the project's GitHub releases.

  livecheck do
    url :stable
    strategy :github_latest
  end

  def install
    bin.install "fetchart-windows.exe" => "fetchart.exe"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/fetchart --version")
  end
end
