#ifndef EXTRACTORJSON_H
#define EXTRACTORJSON_H

#include <QObject>
#include "bloom_filter.h"

class ExtractorJson : public QObject
{
    Q_OBJECT
public:
    explicit ExtractorJson(QObject *parent = nullptr);

signals:

public slots:
    void startParse();

private:
    bloom_filter* bf;

    void parse(QString filename);
};

#endif // EXTRACTORJSON_H
