#include <QtCore>
#include <QDebug>
#include <QSharedPointer>

#include "downloader.h"
// #include "extractor.h"
#include "extractorjson.h"

int main(int argc, char *argv[])
{
  QCoreApplication app(argc, argv);

  // QSharedPointer<Downloader> downloader(new Downloader);

//  create_idfile("");

  ExtractorJson e;
  e.startParse();

//  Extractor e;
//  e.start_extract();

#if 0
  QFile file(".\\ioslogs\\10.10.29.15.2017-05-31-H22log.bak");
  file.open(QIODevice::ReadOnly);

  QFile out_file(".\\ioslogs\\test.log");
  out_file.open(QIODevice::WriteOnly);

  QByteArray data = file.read(1024*1024*1024);
  out_file.write(data);
  file.close();
  out_file.close();
#endif
  qDebug() << "finish!";

  return app.exec();
}
