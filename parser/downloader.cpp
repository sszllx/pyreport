#include "downloader.h"

#include <QUrl>
#include <QtNetwork>

#define CHECK_UPDATE_INTERVAL 1000 * 60 * 60 // 1 hour
// #define LOG_ADDR "http://123.59.43.13:8088/"
#define LOG_ADDR "http://172.16.160.220/res/"
#define OUTPUT_DIR "/out/"

Downloader::Downloader(QObject *parent)
    : QObject(parent),
      timer(new QTimer),
      reply(Q_NULLPTR)
{
    connect(&download_manager, &QNetworkAccessManager::finished,
            this, &Downloader::downloadFinished);

    connect(timer, &QTimer::timeout, this, &Downloader::check_update);
    timer->setInterval(CHECK_UPDATE_INTERVAL);
    timer->start();

    check_update();
}

void Downloader::httpFinished()
{
    reply->deleteLater();
    reply = Q_NULLPTR;

#if 0
    QFile file("test.ttt");
    QTextStream out(&file);
    file.open(QIODevice::WriteOnly);
    out << web_data;
    qDebug() << "write complete";
#endif

    // TODO: 需要判断是否是第一次运行downloader
    parse();
    start_download();
}

void Downloader::httpReadyRead()
{
    web_data += reply->readAll();
}

void Downloader::downloadFinished(QNetworkReply *reply)
{
    QUrl url = reply->url();
    if (reply->error()) {
        fprintf(stderr, "Download of %s failed: %s\n",
                url.toEncoded().constData(),
                qPrintable(reply->errorString()));
    } else {
        QString filename = saveFileName(url);

        QString out_dir = qApp->applicationDirPath() + OUTPUT_DIR;
        QDir dir(out_dir);
        if (!dir.exists()) {
            dir.mkdir(out_dir);
            dir.mkdir(out_dir + "/logs/");
        }

        filename = qApp->applicationDirPath() + OUTPUT_DIR + filename;
        if (saveToDisk(filename, reply)) {
            printf("Download of %s succeeded (saved to %s)\n",
                   url.toEncoded().constData(), qPrintable(filename));

            // TODO: decompress zip
#ifdef Q_OS_WIN32
            QProcess process;
            process.start("C:\\Program Files\\WinRAR\\WinRAR.exe",
                          QStringList() << "e" << filename
                          << qApp->applicationDirPath() + OUTPUT_DIR + "/logs/");
            process.waitForFinished();
            QString output = process.readAll();
            qDebug() << output;
#endif
            url_map[url.toString()] = true;
        }
    }

    currentDownloads.removeAll(reply);
    reply->deleteLater();
}

void Downloader::check_update()
{
    QUrl url(LOG_ADDR);
    reply = qnam.get(QNetworkRequest(url));
    connect(reply, &QNetworkReply::finished, this, &Downloader::httpFinished);
    connect(reply, &QIODevice::readyRead, this, &Downloader::httpReadyRead);
}

void Downloader::parse()
{
    if (url_map.size() == 0) {
        init_url_pair();
        return;
    }

    // TODO: cont.
    QStringList tmp_urls;
    tmp_urls = get_urls();

    foreach(QString url, tmp_urls) {
        QString addr = LOG_ADDR + url;
        if (!url_map.contains(addr)) {
            url_map[addr] = false;
        }
    }
}

void Downloader::init_url_pair()
{
    QStringList tmp_urls;
    tmp_urls = get_urls();

    foreach(QString url, tmp_urls) {
        url_map[LOG_ADDR + url] = false;
    }
}

QStringList Downloader::get_urls()
{
    QStringList tmp_urls;

    int index = 0;
    // for tests
    index = web_data.indexOf("<img src=\"", index);
    index += 1;
    index = web_data.indexOf("<img src=\"", index);
    index += 1;
    index = web_data.indexOf("<img src=\"", index);
    index += 1;
    // end tests
    while ((index = web_data.indexOf("<a href=\"", index)) >= 0) {
        index += 9;
        int end_pos = web_data.indexOf("\">", index);
        QString url = web_data.mid(index, end_pos - index);
        if (url == "../" || url == "abc.txt") {
            continue;
        }
        tmp_urls << url;
    }

    return tmp_urls;
}

void Downloader::start_download()
{
    QMap<QString, bool>::iterator iter = url_map.begin();
    while (iter != url_map.end()) {
        if (!iter.value()) {
            do_download(QUrl(iter.key()));
        }
        ++iter;
    }
}

void Downloader::do_download(QUrl url)
{
    QNetworkRequest request(url);
    QNetworkReply *reply = download_manager.get(request);

    static bool test = false;
    if (!test) {
        currentDownloads.append(reply);
        test = true;
    }
}

bool Downloader::saveToDisk(const QString &filename, QIODevice *data)
{
    QFile file(filename);
    if (!file.open(QIODevice::WriteOnly)) {
        fprintf(stderr, "Could not open %s for writing: %s\n",
                qPrintable(filename),
                qPrintable(file.errorString()));
        return false;
    }

    file.write(data->readAll());
    file.close();

    return true;
}

QString Downloader::saveFileName(const QUrl &url)
{
    QString path = url.path();
    QString basename = QFileInfo(path).fileName();

    if (basename.isEmpty())
        basename = "download";

    if (QFile::exists(basename)) {
        // already exists, don't overwrite
        int i = 0;
        basename += '.';
        while (QFile::exists(basename + QString::number(i)))
            ++i;

        basename += QString::number(i);
    }

    return basename;
}
