function sendMessage(tcpipServer,jsonBytes)
%SENDMESSAGE この関数の概要をここに記述
%   詳細説明をここに記述
fragmentSize = 4096;
fragmentNum = ceil(length(jsonBytes) / fragmentSize);
for j = 1:fragmentNum
    startIdx = (j-1) * fragmentSize + 1;
    endIdx = min(j * fragmentSize, length(jsonBytes));

    write(tcpipServer, jsonBytes(startIdx:endIdx), 'uint8');
end
write(tcpipServer, uint8(0), 'uint8');
end

