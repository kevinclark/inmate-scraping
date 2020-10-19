require 'pry'
require 'http'
require 'nokogiri'
require './nh/names'
require 'time'

# curl 'https://business.nh.gov/Inmate_locator/default.aspx' \
#       -H 'Connection: keep-alive' \
#       -H 'Cache-Control: max-age=0' \
#       -H 'Upgrade-Insecure-Requests: 1' \
#       -H 'Origin: https://business.nh.gov'
#       -H 'Content-Type: application/x-www-form-urlencoded' \
#       -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' \
#       -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
#       -H 'Sec-Fetch-Site: same-origin' \
#       -H 'Sec-Fetch-Mode: navigate' \
#       -H 'Sec-Fetch-User: ?1' \
#       -H 'Sec-Fetch-Dest: document' \
#       -H 'Referer: https://business.nh.gov/Inmate_locator/default.aspx' \
#       -H 'Cookie: pub=78' \
#       --data-raw '__VIEWSTATE=%2FwEPDwUKLTYwNjY5NTU3NA9kFgJmD2QWAgIDD2QWAgIBD2QWBAIBDw9kFgIeBXN0eWxlBQ9kaXNwbGF5OmlubGluZTsWBAIFDw9kFgIeB29uY2xpY2sFEXJldHVybiBmY25DaGVjaygpZAIHDxYCHwAFNHdpZHRoOjEwMCU7dGV4dC1hbGlnbjpjZW50ZXI7Y29sb3I6UmVkO2Rpc3BsYXk6bm9uZTtkAgMPD2QWAh8ABQ1kaXNwbGF5Om5vbmU7ZGQbwMLY9niEF5ODPJTTKG29H5Fowg%3D%3D&__VIEWSTATEGENERATOR=E80E49F3&__EVENTVALIDATION=%2FwEWBAKm7uy9BALXt5DDBgLXt%2Fi4BgK6ouyNC2rWqNZ5xReM4jI%2B5pA3cq4vqhqW&ctl00%24cphMain%24txtLName=wi&ctl00%24cphMain%24txtFName=&ctl00%24cphMain%24btnSubmit=Search'

module Download
  PREFIX_LIST = LastName.prefix(2)
  INMATE_URI  = 'https://business.nh.gov/Inmate_locator/default.aspx'
  HEADERS = {
    connection: 'keep-alive',
    cache_control: 'max-age=0',
    upgrade_insecure_requests: '1',
    origin: 'https://business.nh.gov',
    content_type: 'application/x-www-form-urlencoded',
    user_agent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    sec_fetch_site: 'same-origin',
    sec_fetch_mode: 'navigate',
    sec_fetch_user: '?1',
    sec_fetch_dest: 'document',
    referer: 'https://business.nh.gov/Inmate_locator/default.aspx',
    cookie: 'pub=78'
  }

  ADDRESSES = {
    "NH State Prison for Men" => 'NH State Prison, PO Box 14, Concord, NH 03302',
    "NH Correctional Facility for Women" => 'NHCFW, 42 Perimeter Road, Concord, NH 03301',
    "Northern NH Correctional Facility" => 'Northern NH Correctional Facility, 138 East Milan Road, Berlin, NH 03570'
  }

  def self.list_all
    Dir['./nh/data/*.html'].map do |f|
      data = Nokogiri.parse(File.open(f, 'r'))
      data.xpath('//tr[@style="background-color:#EBF7FB;"]').map do |r|
        row = Nokogiri.parse(r.to_s).xpath('//span')

        address = ADDRESSES[row[9].content]

        next if address.nil?

        if row.size == 9
          {
            first: row[0].content,
            middle: row[1].content,
            last: row[2].content,
            suffix: nil,
            age: row[3].content.to_i,
            inmate_id: row[4].content,
            facility: row[9].content,
            address: address
          }
        else
          {
            first: row[0].content,
            middle: row[1].content,
            last: row[2].content,
            suffix: row[3].content,
            age: row[4].content.to_i,
            inmate_id: row[5].content,
            facility: row[9].content,
            address: address
          }
        end
      end
    end.flatten.compact
  end

  def self.retrieve_all
    PREFIX_LIST.each do |prefix|
      resp = request(prefix: prefix)

      if resp.status == 200
        file = File.new("./nh/data/#{prefix}-#{Time.now.to_i}.html", "w+")
        body = resp.body.to_s
        file.puts body
        file.close
        data = Nokogiri.parse(body)
        data.xpath('//tr[@style="background-color:#EBF7FB;"]').each do |row|
          puts row.content
        end
      else
        puts "#{resp.status}\n#{resp.content}"
      end
    end
  end

  def self.request(prefix:)
    HTTP.headers(HEADERS).post(INMATE_URI, body: body(prefix: prefix))
  end

  def self.body(prefix:)
    "__VIEWSTATE=%2FwEPDwUKLTYwNjY5NTU3NA9kFgJmD2QWAgIDD2QWAgIBD2QWBAIBDw9kFgIeBXN0eWxlBQ9kaXNwbGF5OmlubGluZTsWBAIFDw9kFgIeB29uY2xpY2sFEXJldHVybiBmY25DaGVjaygpZAIHDxYCHwAFNHdpZHRoOjEwMCU7dGV4dC1hbGlnbjpjZW50ZXI7Y29sb3I6UmVkO2Rpc3BsYXk6bm9uZTtkAgMPD2QWAh8ABQ1kaXNwbGF5Om5vbmU7ZGQbwMLY9niEF5ODPJTTKG29H5Fowg%3D%3D&__VIEWSTATEGENERATOR=E80E49F3&__EVENTVALIDATION=%2FwEWBAKm7uy9BALXt5DDBgLXt%2Fi4BgK6ouyNC2rWqNZ5xReM4jI%2B5pA3cq4vqhqW&ctl00%24cphMain%24txtLName=#{prefix}&ctl00%24cphMain%24txtFName=&ctl00%24cphMain%24btnSubmit=Search"
  end
end
