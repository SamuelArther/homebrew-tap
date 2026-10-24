class Fetchart < Formula
  desc "Download game art, achievements, posters, album covers and more from the command line"
  homepage "https://github.com/SamuelArther/fetchart"
  # Windows (brew-windows) installs the standalone build; macOS and Linux build the PyPI package below.
  url "https://github.com/SamuelArther/fetchart/releases/download/v1.5.0/fetchart-windows.exe"
  sha256 "0782758399782cd548e2987ec326920aae6f756eff5c9690a8ee305a7a6c349f"
  license "MIT"

  livecheck do
    url "https://pypi.org/pypi/fetchart/json"
    strategy :json do |json|
      json["info"]["version"]
    end
  end

  on_macos do
    url "https://files.pythonhosted.org/packages/fc/13/12db2e8d879a93ff8b38ae1c05a7bfc9442970a1b12ebc0b16a38438e9b3/fetchart-1.5.0.tar.gz"
    sha256 "0cb32484b48a053c1730d44d24bc0865cc4075042779654161f32bea64ad223f"

    depends_on "pillow"
    depends_on "python@3.14"
  end

  on_linux do
    url "https://files.pythonhosted.org/packages/fc/13/12db2e8d879a93ff8b38ae1c05a7bfc9442970a1b12ebc0b16a38438e9b3/fetchart-1.5.0.tar.gz"
    sha256 "0cb32484b48a053c1730d44d24bc0865cc4075042779654161f32bea64ad223f"

    depends_on "pillow"
    depends_on "python@3.14"
  end

  def install
    if OS.mac? || OS.linux?
      # Homebrew's Python helpers, brought in here rather than with a class-level include: older
      # brew-windows builds don't have them and would fail just loading the formula.
      extend Language::Python::Virtualenv
      virtualenv_install_with_resources
    else
      bin.install "fetchart-windows.exe" => "fetchart.exe"
    end
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/fetchart --version")
  end
end
