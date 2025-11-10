# Tinybeans Downloader

Downloads original quality images from Tinybeans photo journals.

### Quickstart

Installing in `/opt/tinybeans` with a dedicated user:

```bash
sudo mkdir /opt/tinybeans
sudo groupadd tinybeans
sudo useradd tinybeans -g tinybeans
sudo chown -R tinybeans:tinybeans /opt/tinybeans
git clone https://github.com/brege/tinybeans-sync /opt/tinybeans
```

Creating a virtual environment and installing requirements:

```bash
cd /opt/tinybeans
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Prepare the data directory:

```bash
mkdir /var/lib/tinybeans-sync
sudo chown -R tinybeans:tinybeans /var/lib/tinybeans-sync
cp config.yaml.example /var/lib/tinybeans-sync/config.yaml
```

After copying `config.yaml.example` to `/var/lib/tinybeans-sync/config.yaml`, fill in your 
- **email**
- **password**
- **tinybeans_id** (you can get this from journal URLs)

## Usage

Download images from last successful date onwards:
```bash
python cli.py --from-last-date    # --data /var/lib/tinybeans-sync
```

Download a date range:
```bash
python cli.py --after 2025-06-01 --before 2025-08-31
```

Catch up from a specific day through today:
```bash
python cli.py --after 2025-10-27
```

Force re-download (ignores history):
```bash
python cli.py --after 2025-06-01 --force
```

## Configuration

Edit `config.yaml` to customize:
- Output directory (ensure its writable by the user you are running `tinybeans-sync` as)
- Filename patterns (uses `{date}` and `{time}` placeholders)
- Timestamp fixing to match photo dates
- Thumbnail filtering for videos (videos are not yet supported)
- Logging level/target (defaults to `/var/lib/tinybeans-sync/logs/tinybeans-sync.log`)

## History

Downloaded files are tracked in `/var/lib/tinybeans-sync/tinybeans_history.json` to avoid re-downloading deleted images.

Delete that history file to start fresh, or rerun with `--after <date>` to start from a specific date.  Use `--force` to restore image files from a date range or over a date range via `--before` and `--after`.

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)
