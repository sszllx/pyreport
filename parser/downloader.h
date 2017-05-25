#ifndef DOWNLOADER_H
#define DOWNLOADER_H

#include <QNetworkAccessManager>
#include <QObject>
#include <QPair>
#include <QStringList>
#include <QTimer>

class Downloader : public QObject
{
    Q_OBJECT
public:
    explicit Downloader(QObject *parent = 0);

signals:

public slots:
    void httpFinished();
    void httpReadyRead();
    void downloadFinished(QNetworkReply *reply);

private:
    QMap<QString, bool> url_map;
    QTimer *timer;
    QNetworkAccessManager qnam;
    QNetworkAccessManager download_manager;
    QNetworkReply *reply;
    QString web_data;
    QList<QNetworkReply *> currentDownloads;

    void check_update();
    void parse();
    void init_url_pair();
    QStringList get_urls();
    void start_download();
    void do_download(QUrl url);
    bool saveToDisk(const QString &filename, QIODevice *data);
    QString saveFileName(const QUrl &url);
    void write_to_file();
};

#endif // DOWNLOADER_H
