class Fetchamiibo < Formula
  desc "Download amiibo NFC dumps for a Flipper Zero, by name or by game and letter"
  homepage "https://github.com/SamuelArther/fetchamiibo"
  # Windows (brew-windows) installs the standalone build; macOS and Linux build the tagged source below.
  url "https://github.com/SamuelArther/fetchamiibo/releases/download/v1.0.0/fetchamiibo-windows.exe"
  sha256 "c918eb82de7c8e7d763b81760992a8fcfbbe98119b2ea9f5b2fe719f0bbe5cbf"
  license "MIT"

  livecheck do
    url :homepage
    strategy :github_latest
  end

  on_macos do
    url "https://github.com/SamuelArther/fetchamiibo/archive/refs/tags/v1.0.0.tar.gz"
    sha256 "15a40a055e643bd2c76b46e30c14724687abb24bb2da9f01ee512b18755de5a3"

    depends_on "python@3.14"
  end

  on_linux do
    url "https://github.com/SamuelArther/fetchamiibo/archive/refs/tags/v1.0.0.tar.gz"
    sha256 "15a40a055e643bd2c76b46e30c14724687abb24bb2da9f01ee512b18755de5a3"

    depends_on "python@3.14"
  end

  def install
    if OS.mac? || OS.linux?
      # Homebrew's Python helpers, brought in here rather than with a class-level include: older
      # brew-windows builds don't have them and would fail just loading the formula.
      extend Language::Python::Virtualenv
      virtualenv_install_with_resources
    else
      bin.install "fetchamiibo-windows.exe" => "fetchamiibo.exe"
    end
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/fetchamiibo --version")
    assert_match "Super Smash Bros.\tIsabelle", shell_output("#{bin}/fetchamiibo --list")
  end
end
